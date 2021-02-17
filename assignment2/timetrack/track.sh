#!/bin/bash

## comment: export (for making a permanent environment variable) did not comply
#log_path="∼/.local/share/"
#LOGFILE="timetrack.log"
#export $LOGFILE

## comment: opted for the below instead
# check whether LOGFILE has length equal to zero.
if [[ -z "${LOGFILE}" ]]; then
  LOGFILE="timetrack.log"
else
  LOGFILE="${LOGFILE}"
fi

# make logfile if it not exists
if [ ! -e "$LOGFILE" ]; then
    touch $LOGFILE
fi

function track() {

  if [ $# -eq 0 ]; then
    track help  # Show help if no arguments
  else
    case "$1" in
      help)
        echo " "
        echo "track - time tracker"
        echo " "
        echo "Track time spent on a task. Allows one task active per session."
        echo " "
        echo "usage: track                  # show this help"
        echo "usage: track help             # show this help"
        echo "usage: track start [label]    # start tracker and label task [optional]"
        echo "usage: track stop             # stop tracker"
        echo "usage: track status           # display task if one is active"
        echo "usage: track log              # output time spent on task(s)"
        ;;

      start)
        last_entry=$(awk 'END{print $1}' $LOGFILE)  # Should be either LABEL or empty
        if [ "$last_entry" == "" ]; then
          # start new task
          START_TIME=$(date "+%Y-%m-%d %H:%M:%S")
          if [ "$#" == "2" ]; then
            LABEL="$2"
          else
            declare -i LABELCOUNT  # define integer variable
            LABELCOUNT=$(grep -c "LABEL" $LOGFILE)+1  # parse logfile to find number of labels and add 1
            LABEL="Task $LABELCOUNT"
          fi
          echo "START $START_TIME" >> $LOGFILE
          echo "LABEL $LABEL" >> $LOGFILE
        else
          echo "Active task. End before starting a new."
        fi
        ;;

      stop)
        last_entry=$(awk 'END{print $1}' $LOGFILE)  # Should be either LABEL or empty
        if [ "$last_entry" == "LABEL" ]; then
          END_TIME=$(date "+%Y-%m-%d %H:%M:%S")
          echo "END $END_TIME" >> $LOGFILE
          echo " " >> $LOGFILE
        else
          echo "No active task to end."
        fi
        ;;

      status)
        last_entry=$(awk 'END{print $1}' $LOGFILE)  # This should be either LABEL or empty
        if [ "$last_entry" == "LABEL" ]; then
           echo "Active task: $(cat $LOGFILE | grep "LABEL" | tail -n 1 | awk '{$1=""; print substr($0,2)}')"
        else
          echo "No active task.";
        fi
        ;;

      log)
        IFS=$'\n'
        _start_times=($(grep -E "START" $LOGFILE | cut -d' ' -f2-3))  # note use of (...) for array creation
        _labels=($(grep -E "LABEL" $LOGFILE | cut -d' ' -f2-))
        _end_times=($(grep -E "END" $LOGFILE | cut -d' ' -f2-3))

        len=${#_end_times[*]}  # use the length of end times so only ended tasks are included
        for (( i=0; i<${len}; i++ )); do
          if [ "$(uname)" == "Darwin" ]; then
            _start_time=$(gdate -d "${_start_times[$i]}" '+%s')
            _end_time=$(gdate -d "${_end_times[$i]}" '+%s')
            _elapsed_time=$(($_end_time-$_start_time))
            task_time=$(printf "%02d:%02d:%02d\n" $(($_elapsed_time/3600)) $(($_elapsed_time%3600/60)) $(($_elapsed_time%60)))
            echo "${_labels[$i]}: $task_time"
          elif [ "$(uname)" == "Linux" ]; then
            _start_time=$(date -d "${_start_times[$i]}" '+%s')
            _end_time=$(date -d "${_end_times[$i]}" '+%s')
            _elapsed_time=$(($_end_time-$_start_time))
            task_time=$(printf "%02d:%02d:%02d\n" $(($_elapsed_time/3600)) $(($_elapsed_time%3600/60)) $(($_elapsed_time%60)))
            echo "${_labels[$i]}: $task_time"
          else
            echo "The log command is currently not supported on your operating system"
          fi
        done
        ;;

      *)
         echo $"Usage: $0 {start [label]|stop|status|log|help}"
         exit 1
    esac
  fi

}

# Main
track "$@"
