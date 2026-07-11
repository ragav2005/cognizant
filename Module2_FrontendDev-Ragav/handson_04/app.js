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


function fetchUser(id) {
    return fetch(`https://jsonplaceholder.typicode.com/users/${id}`)
        .then(response => response.json())
        .then(user => {
            console.log("Promise User:", user.name);
            return user;
        });
}

fetchUser(1);


async function fetchUserAsync(id) {
    try {
        const response = await fetch(
            `https://jsonplaceholder.typicode.com/users/${id}`
        );

        const user = await response.json();

        console.log("Async User:", user.name);

    } catch (error) {

        console.error(error);

    }
}

fetchUserAsync(2);

const loadingCourses = document.getElementById("loading-courses");

async function fetchAllCourses() {

    loadingCourses.style.display = "block";

    return new Promise(resolve => {

        setTimeout(() => {

            loadingCourses.style.display = "none";

            resolve(courses);

        }, 1000);

    });

}

fetchAllCourses().then(courseData => {

    renderCourses(courseData);

});


Promise.all([

    fetchUser(1),
    fetchUser(2)

]).then(users => {

    console.log(
        "Both Users:",
        users.map(user => user.name)
    );

});

async function apiFetch(url) {

    const response = await fetch(url);

    if (!response.ok) {

        throw new Error(
            `Error ${response.status}: ${response.statusText}`
        );

    }

    return await response.json();

}

const notificationList =
    document.getElementById("notification-list");

const spinner =
    document.getElementById("spinner");

const errorMessage =
    document.getElementById("error-message");

const retryButton =
    document.getElementById("retry-btn");

async function loadNotifications() {

    spinner.style.display = "block";

    notificationList.innerHTML = "";

    errorMessage.textContent = "";

    retryButton.style.display = "none";

    try {

        const posts = await apiFetch(
            "https://jsonplaceholder.typicode.com/posts?_limit=5"
        );

        spinner.style.display = "none";

        posts.forEach(post => {

            const card = document.createElement("article");

            card.className = "course-card";

            card.innerHTML = `
                <h3>${post.title}</h3>
                <p>${post.body}</p>
            `;

            notificationList.appendChild(card);

        });

    }

    catch (error) {

        spinner.style.display = "none";

        errorMessage.textContent =
            "Unable to load notifications.";

        retryButton.style.display = "inline-block";

    }

}

loadNotifications();

const simulate404 = async () => {

    try {

        await apiFetch(
            "https://jsonplaceholder.typicode.com/nonexistent"
        );

    }

    catch (error) {

        errorMessage.textContent =
            "404 Error: Resource not found.";

        retryButton.style.display = "inline-block";

    }

};

simulate404();

retryButton.addEventListener("click", () => {

    loadNotifications();

});

axios.interceptors.request.use(config => {

    console.log("API call started:", config.url);

    return config;

});

async function axiosFetch(url) {

    const response = await axios.get(url);

    return response.data;

}

async function loadUserPosts() {

    try {
        const posts = await axiosFetch(
            "https://jsonplaceholder.typicode.com/posts?userId=1"
        );
        console.log(
            "User 1 Posts:",
            posts
        );
    }

    catch (error) {
        console.error(error);
    }
}

loadUserPosts();
