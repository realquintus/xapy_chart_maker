<?php
$activity_id = $_GET["activity_id"];
$completion_needed = $_GET["completion_needed"];
if( $_GET['learner_id'] != ""){
        $learner_id = "-l ".$_GET["learner_id"];
}
else{
        $learner_id = "";
}
if($_GET['return_type'] == "chart"){
        $type = "-c";
}
else{
        $type = "-t";
}
$output = shell_exec("python3 ./xapy_chart_maker/main.py -a $activity_id -n $completion_needed $learner_id $type 2>&1");
echo($output);
?>