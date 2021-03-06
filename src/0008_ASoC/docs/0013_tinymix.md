# tinymix

主要是分析tinymix如何获取声卡的controls以及如果要操作control的时候，系统的调用流程

# tinymix分析

```C
#include <tinyalsa/asoundlib.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <ctype.h>
#include <string.h>
#include <limits.h>

static void tinymix_list_controls(struct mixer *mixer, int print_all);

static void tinymix_detail_control(struct mixer *mixer, const char *control);

static void tinymix_set_value(struct mixer *mixer, const char *control,
                              char **values, unsigned int num_values);

static void tinymix_print_enum(struct mixer_ctl *ctl);

void usage(void)
{
    printf("usage: tinymix [options] <command>\n");
    printf("options:\n");
    printf("\t-h, --help        : prints this help message and exists\n");
    printf("\t-v, --version     : prints this version of tinymix and exists\n");
    printf("\t-D, --card NUMBER : specifies the card number of the mixer\n");
    printf("commands:\n");
    printf("\tget NAME|ID       : prints the values of a control\n");
    printf("\tset NAME|ID VALUE : sets the value of a control\n");
    printf("\tcontrols          : lists controls of the mixer\n");
    printf("\tcontents          : lists controls of the mixer and their contents\n");
}

void version(void)
{
    printf("tinymix version 2.0 (tinyalsa version %s)\n", TINYALSA_VERSION_STRING);
}

int main(int argc, char **argv)
{
    struct mixer *mixer;
    int card = 0;
    char *cmd;

    while (1) {
        static struct option long_options[] = {
            { "version", no_argument, NULL, 'v' },
            { "help",    no_argument, NULL, 'h' },
            { 0, 0, 0, 0 }
        };

        /* getopt_long stores the option index here. */
        int option_index = 0;
        int c = 0;

        c = getopt_long (argc, argv, "c:D:hv", long_options, &option_index);

        /* Detect the end of the options. */
        if (c == -1)
            break;

        switch (c) {
        case 'D':
            card = atoi(optarg);
            break;
        case 'h':
            usage();
            return EXIT_SUCCESS;
        case 'v':
            version();
            return EXIT_SUCCESS;
        }
    }

    /**
     * snprintf(fn, sizeof(fn), "/dev/snd/controlC%u", card);
     *
     * 1. 打开张网卡的control；
     * 2. ioctl获取SNDRV_CTL_IOCTL_CARD_INFO信息；
     *   if (ioctl(fd, SNDRV_CTL_IOCTL_CARD_INFO, &mixer->card_info) < 0)
     * 3. 获取所有的controls；
     *   if (add_controls(mixer) != 0)
     * 4. 获取了驱动中&card->controls中注册的control；
     */
    mixer = mixer_open(card);
    if (!mixer) {
        fprintf(stderr, "Failed to open mixer\n");
        return EXIT_FAILURE;
    }

    cmd = argv[optind];
    if (cmd == NULL) {
        fprintf(stderr, "no command specified (see --help)\n");
        mixer_close(mixer);
        return EXIT_FAILURE;
    } else if (strcmp(cmd, "get") == 0) {
        if ((optind + 1) >= argc) {
            fprintf(stderr, "no control specified\n");
            mixer_close(mixer);
            return EXIT_FAILURE;
        }
        tinymix_detail_control(mixer, argv[optind + 1]);                            // mixer_open已经获取了所有的controls了，这里只是解析一下；
        printf("\n");
    } else if (strcmp(cmd, "set") == 0) {
        if ((optind + 1) >= argc) {
            fprintf(stderr, "no control specified\n");
            mixer_close(mixer);
            return EXIT_FAILURE;
        }
        if ((optind + 2) >= argc) {
            fprintf(stderr, "no value(s) specified\n");
            mixer_close(mixer);
            return EXIT_FAILURE;
        }
        tinymix_set_value(mixer, argv[optind + 1], &argv[optind + 2], argc - optind - 2);       // 这个软件主要是跟这个函数怎么工作的
    } else if (strcmp(cmd, "controls") == 0) {
        tinymix_list_controls(mixer, 0);
    } else if (strcmp(cmd, "contents") == 0) {
        tinymix_list_controls(mixer, 1);
    } else {
        fprintf(stderr, "unknown command '%s' (see --help)\n", cmd);
        mixer_close(mixer);
        return EXIT_FAILURE;
    }

    mixer_close(mixer);
    return EXIT_SUCCESS;
}

static void tinymix_list_controls(struct mixer *mixer, int print_all)
{
    struct mixer_ctl *ctl;
    const char *name, *type;
    unsigned int num_ctls, num_values;
    unsigned int i;

    num_ctls = mixer_get_num_ctls(mixer);

    printf("Number of controls: %u\n", num_ctls);

    if (print_all)
        printf("ctl\ttype\tnum\t%-40svalue\n", "name");
    else
        printf("ctl\ttype\tnum\t%-40s\n", "name");

    for (i = 0; i < num_ctls; i++) {
        ctl = mixer_get_ctl(mixer, i);

        name = mixer_ctl_get_name(ctl);
        type = mixer_ctl_get_type_string(ctl);
        num_values = mixer_ctl_get_num_values(ctl);
        printf("%u\t%s\t%u\t%-40s", i, type, num_values, name);
        if (print_all)
            tinymix_detail_control(mixer, name);
        printf("\n");
    }
}

static void tinymix_print_enum(struct mixer_ctl *ctl)
{
    unsigned int num_enums;
    unsigned int i;
    unsigned int value;
    const char *string;

    num_enums = mixer_ctl_get_num_enums(ctl);
    value = mixer_ctl_get_value(ctl, 0);

    for (i = 0; i < num_enums; i++) {
        string = mixer_ctl_get_enum_string(ctl, i);
        printf("%s%s, ", value == i ? "> " : "", string);
    }
}

// 这一段代码都是从controls缓冲中获取一个control的信息，controls缓冲是在control设备文件打开的时候获取的；
static void tinymix_detail_control(struct mixer *mixer, const char *control)
{
    struct mixer_ctl *ctl;
    enum mixer_ctl_type type;
    unsigned int num_values;
    unsigned int i;
    int min, max;
    int ret;
    char *buf = NULL;
    unsigned int tlv_header_size = 0;

    if (isdigit(control[0]))
        ctl = mixer_get_ctl(mixer, atoi(control));
    else
        ctl = mixer_get_ctl_by_name(mixer, control);

    if (!ctl) {
        fprintf(stderr, "Invalid mixer control\n");
        return;
    }

    type = mixer_ctl_get_type(ctl);
    num_values = mixer_ctl_get_num_values(ctl);

    if ((type == MIXER_CTL_TYPE_BYTE) && (num_values > 0)) {
        if (mixer_ctl_is_access_tlv_rw(ctl) != 0) {
            tlv_header_size = TLV_HEADER_SIZE;
        }
        buf = calloc(1, num_values + tlv_header_size);
        if (buf == NULL) {
            fprintf(stderr, "Failed to alloc mem for bytes %u\n", num_values);
            return;
        }

        ret = mixer_ctl_get_array(ctl, buf, num_values + tlv_header_size);
        if (ret < 0) {
            fprintf(stderr, "Failed to mixer_ctl_get_array\n");
            free(buf);
            return;
        }
    }

    for (i = 0; i < num_values; i++) {
        switch (type)
        {
        case MIXER_CTL_TYPE_INT:
            printf("%d", mixer_ctl_get_value(ctl, i));
            break;
        case MIXER_CTL_TYPE_BOOL:
            printf("%s", mixer_ctl_get_value(ctl, i) ? "On" : "Off");
            break;
        case MIXER_CTL_TYPE_ENUM:
            tinymix_print_enum(ctl);
            break;
        case MIXER_CTL_TYPE_BYTE:
            /* skip printing TLV header if exists */
            printf(" %02x", buf[i + tlv_header_size]);
            break;
        default:
            printf("unknown");
            break;
        };
        if ((i + 1) < num_values) {
           printf(", ");
        }
    }

    if (type == MIXER_CTL_TYPE_INT) {
        min = mixer_ctl_get_range_min(ctl);
        max = mixer_ctl_get_range_max(ctl);
        printf(" (range %d->%d)", min, max);
    }

    free(buf);
}

static void tinymix_set_byte_ctl(struct mixer_ctl *ctl,
                                 char **values, unsigned int num_values)
{
    int ret;
    char *buf;
    char *end;
    unsigned int i;
    long n;
    unsigned int *tlv, tlv_size;
    unsigned int tlv_header_size = 0;

    if (mixer_ctl_is_access_tlv_rw(ctl) != 0) {
        tlv_header_size = TLV_HEADER_SIZE;
    }

    tlv_size = num_values + tlv_header_size;

    buf = calloc(1, tlv_size);
    if (buf == NULL) {
        fprintf(stderr, "set_byte_ctl: Failed to alloc mem for bytes %u\n", num_values);
        exit(EXIT_FAILURE);
    }

    tlv = (unsigned int *)buf;
    tlv[0] = 0;
    tlv[1] = num_values;

    for (i = 0; i < num_values; i++) {
        errno = 0;
        n = strtol(values[i], &end, 0);
        if (*end) {
            fprintf(stderr, "%s not an integer\n", values[i]);
            goto fail;
        }
        if (errno) {
            fprintf(stderr, "strtol: %s: %s\n", values[i],
                strerror(errno));
            goto fail;
        }
        if (n < 0 || n > 0xff) {
            fprintf(stderr, "%s should be between [0, 0xff]\n",
                values[i]);
            goto fail;
        }
        /* start filling after tlv header */
        buf[i + tlv_header_size] = n;
    }

    ret = mixer_ctl_set_array(ctl, buf, tlv_size);
    if (ret < 0) {
        fprintf(stderr, "Failed to set binary control\n");
        goto fail;
    }

    free(buf);
    return;

fail:
    free(buf);
    exit(EXIT_FAILURE);
}

static int is_int(char *value)
{
    char* end;
    long int result;

    errno = 0;
    result = strtol(value, &end, 10);

    if (result == LONG_MIN || result == LONG_MAX)
        return 0;

    return errno == 0 && *end == '\0';
}

static void tinymix_set_value(struct mixer *mixer, const char *control,
                              char **values, unsigned int num_values)
{
    struct mixer_ctl *ctl;
    enum mixer_ctl_type type;
    unsigned int num_ctl_values;
    unsigned int i;

    if (isdigit(control[0]))                                // 通过数字索引查找还是通过名字查找
        ctl = mixer_get_ctl(mixer, atoi(control));
    else
        ctl = mixer_get_ctl_by_name(mixer, control);

    if (!ctl) {
        fprintf(stderr, "Invalid mixer control\n");
        return;
    }

    type = mixer_ctl_get_type(ctl);                         // 获取当前control的类型
    num_ctl_values = mixer_ctl_get_num_values(ctl);         // 获取当前control的values的个数

    if (type == MIXER_CTL_TYPE_BYTE) {                      // 假装不是
        tinymix_set_byte_ctl(ctl, values, num_values);      // 如果是MIXER_CTL_TYPE_BYTE，那么用这个函数处理
        return;
    }

    if (is_int(values[0])) {                                // 假装是
        if (num_values == 1) {                              // 假装是
            /* Set all values the same */
            int value = atoi(values[0]);                    // 转化为整数

            for (i = 0; i < num_ctl_values; i++) {
                if (mixer_ctl_set_value(ctl, i, value)) {   // 要设置值了，跟进去
                    fprintf(stderr, "Error: invalid value\n");
                    return;
                }
            }
        } else {
            /* Set multiple values */
            if (num_values > num_ctl_values) {
                fprintf(stderr,
                        "Error: %u values given, but control only takes %u\n",
                        num_values, num_ctl_values);
                return;
            }
            for (i = 0; i < num_values; i++) {
                if (mixer_ctl_set_value(ctl, i, atoi(values[i]))) {
                    fprintf(stderr, "Error: invalid value for index %u\n", i);
                    return;
                }
            }
        }
    } else {
        if (type == MIXER_CTL_TYPE_ENUM) {
            if (num_values != 1) {
                fprintf(stderr, "Enclose strings in quotes and try again\n");
                return;
            }
            if (mixer_ctl_set_enum_by_string(ctl, values[0]))
                fprintf(stderr, "Error: invalid enum value\n");
        } else {
            fprintf(stderr, "Error: only enum types can be set with strings\n");
        }
    }
}
```

# [mixer_ctl_set_value](https://github.com/tinyalsa/tinyalsa/src/mixer.c#L726)

```C
int mixer_ctl_set_value(struct mixer_ctl *ctl, unsigned int id, int value)
{
    struct snd_ctl_elem_value ev;
    int ret;

    if (!ctl || (id >= ctl->info.count))
        return -EINVAL;

    memset(&ev, 0, sizeof(ev));                                             // 初始化一个control element
    ev.id.numid = ctl->info.id.numid;
    ret = ioctl(ctl->mixer->fd, SNDRV_CTL_IOCTL_ELEM_READ, &ev);
    if (ret < 0)
        return ret;

    switch (ctl->info.type) {
    case SNDRV_CTL_ELEM_TYPE_BOOLEAN:
        ev.value.integer.value[id] = !!value;
        break;

    case SNDRV_CTL_ELEM_TYPE_INTEGER:
        if ((value < mixer_ctl_get_range_min(ctl)) ||
            (value > mixer_ctl_get_range_max(ctl))) {
            return -EINVAL;
        }

        ev.value.integer.value[id] = value;
        break;

    case SNDRV_CTL_ELEM_TYPE_ENUMERATED:
        ev.value.enumerated.item[id] = value;
        break;

    case SNDRV_CTL_ELEM_TYPE_BYTES:
        ev.value.bytes.data[id] = value;
        break;

    default:
        return -EINVAL;
    }

    /**
     * 最终通过这个调用
     * case SNDRV_CTL_IOCTL_ELEM_WRITE:
     *    return snd_ctl_elem_write_user(ctl, argp);
     */
    return ioctl(ctl->mixer->fd, SNDRV_CTL_IOCTL_ELEM_WRITE, &ev);          
}
```

# [snd_ctl_elem_write_user](https://elixir.bootlin.com/linux/latest/source/sound/core/control.c#L965)调用[snd_ctl_elem_write](https://elixir.bootlin.com/linux/latest/source/sound/core/control.c#L933)

```C
static int snd_ctl_elem_write(struct snd_card *card, struct snd_ctl_file *file,
                  struct snd_ctl_elem_value *control)
{
    struct snd_kcontrol *kctl;
    struct snd_kcontrol_volatile *vd;
    unsigned int index_offset;
    int result;

    kctl = snd_ctl_find_id(card, &control->id);
    if (kctl == NULL)
        return -ENOENT;

    index_offset = snd_ctl_get_ioff(kctl, &control->id);
    vd = &kctl->vd[index_offset];
    if (!(vd->access & SNDRV_CTL_ELEM_ACCESS_WRITE) || kctl->put == NULL ||
        (file && vd->owner && vd->owner != file)) {
        return -EPERM;
    }

    snd_ctl_build_ioff(&control->id, kctl, index_offset);
    result = kctl->put(kctl, control);                                  // <---------最终调用
    if (result < 0)
        return result;

    if (result > 0) {
        struct snd_ctl_elem_id id = control->id;
        snd_ctl_notify(card, SNDRV_CTL_EVENT_MASK_VALUE, &id);
    }

    return 0;
}
```
