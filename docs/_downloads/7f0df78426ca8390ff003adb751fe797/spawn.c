#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <unistd.h>
#include <spawn.h>
#include <sys/wait.h>

void run_cmd(char *args[])
{
    pid_t pid;
    // char *args[] = {"/bin/ip", "tuntap", "add", "dev", "tap1", "mod", "tap", NULL};
    // char *args[] = {"/bin/ip", "link", "set", "dev", "tap0", "up", NULL};
    int status;

    status = posix_spawn(&pid, args[0], NULL, NULL, &args[0], NULL);
    if (status == 0) {
        printf("Child pid: %i\n", pid);
        do {
          if (waitpid(pid, &status, 0) != -1) {
            printf("Child status %d\n", WEXITSTATUS(status));
          } else {
            perror("waitpid");
            exit(1);
          }
        } while (!WIFEXITED(status) && !WIFSIGNALED(status));
    } else {
        printf("posix_spawn: %s\n", strerror(status));
    }

}

void main(int argc, char* argv[])
{
	// ip tuntap add dev tap0 mod tap
    char *args_device[] = {"/bin/ip", "tuntap", "add", "dev", "tap0", "mod", "tap", NULL};
    run_cmd(args_device);
	// ip link set dev tap0 up
    char *args_up[] = {"/bin/ip", "link", "set", "dev", "tap0", "up", NULL};
    run_cmd(args_up);

    return;
}

