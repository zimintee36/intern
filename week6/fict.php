<?php

// 读取 fcit_data.json
$json_file = "fcit_data.json";

$json = file_get_contents($json_file);

$courses = json_decode($json, true);

?>

<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<title>FCIT Courses</title>

<style>

body {
    font-family: Arial, sans-serif;
    background-color: #f5f7fa;
    margin: 40px;
}


.course-card {

    background: white;

    width: 80%;

    margin: 30px auto;

    padding: 25px;

    border-radius: 12px;

    box-shadow: 0 4px 10px rgba(0,0,0,0.1);

}


.course-title {

    color: #003366;

    border-bottom: 3px solid #003366;

    padding-bottom: 10px;

}


.section-title {

    color: #ff6600;

    margin-top: 25px;

}


.details {

    background: #f0f6ff;

    padding: 15px;

    border-radius: 8px;

}


.details p {

    margin: 8px 0;

}


.introduction p {

    line-height: 1.7;

    text-align: justify;

}


.label {

    font-weight: bold;

    color: #003366;

}


hr {

    border: none;

    border-top: 1px solid #ddd;

    margin-top: 30px;

}


</style>

</head>


<body>


<?php


foreach ($courses as $course) {


    echo "<div class='course-card'>";


    // Course Name

    echo "<h2 class='course-title'>";
    
    echo $course["course_name"];

    echo "</h2>";



    // Course Details

    echo "<h3 class='section-title'>";
    
    echo "Course Details";

    echo "</h3>";


    echo "<div class='details'>";


    foreach ($course["course_details"] as $key => $value) {


        echo "<p>";

        echo "<span class='label'>";
        
        echo $key;

        echo ":</span> ";

        echo $value;

        echo "</p>";


    }


    echo "</div>";



    // Course Introduction

    echo "<h3 class='section-title'>";
    
    echo "Course Introduction";

    echo "</h3>";


    echo "<div class='introduction'>";


foreach ($course["course_introduction"] as $intro) {

    // 去除不需要显示的文字
    if (
        $intro == "Partnerships:" ||
        $intro == "Course Introduction"
    ) {
        continue;
    }


    echo "<p>";
    echo $intro;
    echo "</p>";

}


    echo "</div>";



    echo "</div>";

}


?>


</body>
</html>