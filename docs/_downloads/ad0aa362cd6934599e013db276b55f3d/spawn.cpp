#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <string.h>

#include <unistd.h>
#include <spawn.h>
#include <sys/wait.h>
#include <vector>

void run_cmd(std::vector<std::string> argVector)
{
    pid_t pid;
    int status;

	/*
    std::vector<std::string> argVector = {
        "/bin/ip",
        "link",
        "set",
        "dev",
		"tap0",
        "up",
    };
    */

    // const char *args[] = {"/bin/ip", "link", "set", "dev", ifr.ifr_name, "up", NULL};
    std::vector<char*> args(argVector.size() + 1);
    for (unsigned i = 0; i < argVector.size(); i++) {
        args[i] = (char*)argVector[i].c_str();
    }

    status = posix_spawn(&pid, args[0], nullptr, nullptr, &args[0], nullptr);
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

	return;
}

int main(int argc, char* argv[])
{
    std::vector<std::string> argVector_device = {
        "/bin/ip",
        "tuntap",
        "add",
        "dev",
        "tap1",
        "mod",
        "tap",
    };

    std::vector<std::string> argVector_up = {
        "/bin/ip",
        "link",
        "set",
        "dev",
        "tap1",
        "up",
    };

    run_cmd(argVector_device);
    run_cmd(argVector_up);

    return 0;
}

