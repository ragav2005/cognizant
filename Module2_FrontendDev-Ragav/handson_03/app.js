import { courses } from "./data.js";

for (const course of courses) {
    const { name, credits } = course;
    console.log(`${name} - ${credits} credits`);
}


const formattedCourses = courses.map(
    ({ code, name, credits }) =>
        `${code} - ${name} (${credits} credits)`
);

console.log(formattedCourses);


const fourCreditCourses = courses.filter(
    course => course.credits >= 4
);

console.log("Courses with credits >= 4:", fourCreditCourses.length);


const totalCredits = courses.reduce(
    (sum, course) => sum + course.credits,
    0
);

console.log("Total Credits:", totalCredits);


courses.forEach(course =>
    console.log(`${course.name} (${course.code})`)
);

const courseGrid = document.querySelector(".course-grid");
const totalCreditsElement = document.getElementById("total-credits");
export const searchInput = document.getElementById("search-courses");
const sortButton = document.getElementById("sort-btn");
const selectedCourse = document.getElementById("selected-course");


export function renderCourses(courseList) {

    selectedCourse.innerHTML = "";
    selectedCourse.style.display = "none";

    courseGrid.innerHTML = "";

    const fragment = document.createDocumentFragment();

    courseList.forEach(course => {

        const article = document.createElement("article");

        article.className = "course-card";

        article.dataset.id = course.id;

        article.innerHTML = `
            <h3>${course.name}</h3>
            <p><strong>Course Code:</strong> ${course.code}</p>
            <p><strong>Credits:</strong> ${course.credits}</p>
        `;

        fragment.appendChild(article);

    });

    courseGrid.appendChild(fragment);

    totalCreditsElement.textContent =
        `Total Credits Enrolled: ${courseList.reduce(
            (sum, course) => sum + course.credits,
            0
        )}`;
}


renderCourses(courses);


searchInput.addEventListener("input", event => {
    const keyword = event.target.value.toLowerCase();
    const filteredCourses = courses.filter(
        course => course.name.toLowerCase().includes(keyword)
    );
    renderCourses(filteredCourses);
});


sortButton.addEventListener("click", () => {

    const sortedCourses = [...courses].sort(
        (a, b) => b.credits - a.credits
    );

    renderCourses(sortedCourses);

});


courseGrid.addEventListener("click", event => {

    const card = event.target.closest(".course-card");

    if (!card) return;

    const prev = courseGrid.querySelector('.course-card.active');
    if (prev) prev.classList.remove('active');
    card.classList.add('active');

    const id = Number(card.dataset.id);

    const course = courses.find(c => c.id === id);

    selectedCourse.innerHTML = `
        <h3>Selected Course</h3>
        <p><strong>${course.name}</strong></p>
        <p>Grade: ${course.grade}</p>
    `;
    selectedCourse.style.display = 'block';

});
