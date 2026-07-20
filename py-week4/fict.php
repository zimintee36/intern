<?php

// 读取 JSON 文件
$json_file = "fcit_data.json";

if (file_exists($json_file)) {

    $json_data = file_get_contents($json_file);

    $courses = json_decode(
        $json_data,
        true
    );

} else {

    $courses = [];

}

?>

<!DOCTYPE html>
<html>
<head>
    <title>FCIT Courses</title>

    <style>

        body {
            font-family: Arial, sans-serif;
            background: #f2f2f2;
            padding: 30px;
        }


        .course {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
        }


        h2 {
            color: #003366;
        }


        p {
            line-height: 1.6;
        }


    </style>

</head>


<body>


<h1>Faculty of Computing and Information Technology Courses</h1>


<?php


foreach ($courses as $course) {


    echo "<div class='course'>";


    echo "<h2>";

    echo htmlspecialchars(
        $course["course_name"]
    );

    echo "</h2>";



    echo "<h3>Course Introduction</h3>";



    if (
        isset(
            $course["course_introduction"]
        )
    ) {


        foreach (
            $course["course_introduction"]
            as $intro
        ) {


            echo "<p>";

            echo htmlspecialchars(
                $intro
            );

            echo "</p>";


        }


    }



    echo "</div>";

}


?>


</body>
</html>