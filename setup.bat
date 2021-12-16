@echo off
set /p var=PleaseEnterCommitMessage:
call cmd /k " cd/d .\dev &&yarn docs:build && cd/d .. &&XCOPY .\dev\docs\.vuepress\dist  .\docs  /e /d /y && git add -A && git commit -m"%var%"&& git push -u origin master"
