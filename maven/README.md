# create new app
mvn archetype:generate -DgroupId=model_infer -DartifactId=model_infer -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false

# build app
mvn clean package

# run app
java -cp target/model_infer-1.0-SNAPSHOT.jar model_infer.FasterRcnnInception ../testimages/image2.jpg ../images/image2rcnn.jpg 