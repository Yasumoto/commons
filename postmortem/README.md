TO RUN
================

    ./pants py ./src/python/twitter/postmortem:service-a --app_profiling
    ./pants py ./src/python/twitter/postmortem:service-b --app_profiling --http_port=8889
    ./pants goal run ./src/java/com/twitter/postmortem/main --jvm-run-args="-http_port=8890"

Take a look at /vars to see some statistics that are exported by the services.
