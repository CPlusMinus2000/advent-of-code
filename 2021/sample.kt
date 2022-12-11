
// Give me a main function
fun main(args: Array<String>) {
    // Create a variable of type `String` called `myName` and assign it to your name
    val myName = "Sebastian"
    // Create a variable of type `Int` called `myAge` and assign it your age
    val myAge = 28
    // Create a variable of type `Double` called `myHeight` and assign it your height
    val myHeight = 1.75
    // Create a variable of type `String` called `myOccupation` and assign it your occupation
    val myOccupation = "Software Developer"

    // Create a variable of type `String` called `myInfo` and assign it the following string:
    // "My name is <myName> and I am <myAge> years old. I am <myHeight> meters tall and I am a <myOccupation>"
    val myInfo = "My name is $myName and I am $myAge years old. I am $myHeight meters tall and I am a $myOccupation"

    // Print the `myInfo` variable
    println(myInfo)
}