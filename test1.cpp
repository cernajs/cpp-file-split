#include <iostream>
#include <string>

class Student {
public:
    Student(std::string name, int age, std::string major) : name(name), age(age), major(major) {}

    void display() {
        std::cout << "Student: " << name << ", Age: " << age << ", Major: " << major << std::endl;
    }

private:
    std::string name;
    int age;
    std::string major;
};

class Teacher {
public:
    Teacher(std::string name, int age, std::string subject) : name(name), age(age), subject(subject) {}

    void display() {
        std::cout << "Teacher: " << name << ", Age: " << age << ", Subject: " << subject << std::endl;
    }

private:
    std::string name;
    int age;
    std::string subject;
};

int main() {
    Student s("John", 21, "Computer Science");
    s.display();

    Teacher t("Dr. Smith", 45, "Physics");
    t.display();

    return 0;
}