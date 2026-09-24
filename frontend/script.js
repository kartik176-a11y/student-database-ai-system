// ==========================================
// GLOBAL VARIABLES
// ==========================================

let students = [];
let editingStudentId = null;


// ==========================================
// LOAD STUDENTS
// ==========================================

async function loadStudents() {

    try {

        const response = await fetch("/students/");

        if (!response.ok) {
            throw new Error("Failed to load students");
        }

        students = await response.json();

        displayStudents(students);
        updateDashboard(students);

    } catch (error) {

        console.error("Error loading students:", error);

    }
}


// ==========================================
// DISPLAY STUDENTS
// ==========================================

function displayStudents(data) {

    const table = document.getElementById("studentTable");

    if (!table) return;

    table.innerHTML = "";

    data.forEach(student => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${student.id}</td>
            <td>${student.name}</td>
            <td>${student.age}</td>
            <td>${student.gender}</td>
            <td>${student.email}</td>
            <td>${student.course}</td>
            <td>${student.year}</td>
            <td>${student.phone}</td>

            <td>
                <button
                    class="edit-btn"
                    onclick="editStudent(${student.id})">
                    ✏️
                </button>

                <button
                    class="delete-btn"
                    onclick="deleteStudent(${student.id})">
                    🗑️
                </button>
            </td>
        `;

        table.appendChild(row);

    });


    // Dashboard table

    const dashboardTable =
        document.getElementById("dashboardTable");

    if (!dashboardTable) return;

    dashboardTable.innerHTML = "";

    data.slice(-5).reverse().forEach(student => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${student.id}</td>
            <td>${student.name}</td>
            <td>${student.course}</td>
            <td>${student.year}</td>
            <td>${student.email}</td>
        `;

        dashboardTable.appendChild(row);

    });

}


// ==========================================
// DASHBOARD
// ==========================================

function updateDashboard(data) {

    const total =
        document.getElementById("totalStudents");

    const male =
        document.getElementById("maleStudents");

    const female =
        document.getElementById("femaleStudents");

    const courses =
        document.getElementById("courseCount");


    if (total) {

        total.textContent = data.length;

    }


    if (male) {

        male.textContent =
            data.filter(
                student =>
                    student.gender &&
                    student.gender.toLowerCase() === "male"
            ).length;

    }


    if (female) {

        female.textContent =
            data.filter(
                student =>
                    student.gender &&
                    student.gender.toLowerCase() === "female"
            ).length;

    }


    if (courses) {

        const uniqueCourses =
            new Set(
                data.map(student => student.course)
            );

        courses.textContent =
            uniqueCourses.size;

    }

}


// ==========================================
// SECTION NAVIGATION
// ==========================================

function showSection(sectionName) {

    document
        .querySelectorAll(".section")
        .forEach(section => {

            section.classList.remove(
                "active-section"
            );

        });


    const section =
        document.getElementById(sectionName);

    if (section) {

        section.classList.add(
            "active-section"
        );

    }


    document
        .querySelectorAll(".nav-item")
        .forEach(button => {

            button.classList.remove("active");

        });


    document
        .querySelectorAll(".nav-item")
        .forEach(button => {

            if (
                button.getAttribute("onclick") ===
                `showSection('${sectionName}')`
            ) {

                button.classList.add("active");

            }

        });


    const pageTitle =
        document.getElementById("page-title");


    if (pageTitle) {

        if (sectionName === "dashboard") {
            pageTitle.textContent = "Dashboard";
        }

        if (sectionName === "students") {
            pageTitle.textContent = "Students";
        }

        if (sectionName === "chat") {
            pageTitle.textContent = "AI Assistant";
        }

    }

}


// ==========================================
// OPEN ADD STUDENT MODAL
// ==========================================

function openStudentModal() {

    console.log("Add Student button clicked");

    editingStudentId = null;


    const modal =
        document.getElementById("studentModal");

    const form =
        document.getElementById("studentForm");

    const title =
        document.getElementById("modalTitle");


    if (!modal) {

        console.error(
            "studentModal not found"
        );

        return;

    }


    if (form) {

        form.reset();

    }


    const studentId =
        document.getElementById("studentId");


    if (studentId) {

        studentId.value = "";

    }


    if (title) {

        title.textContent =
            "➕ Add Student";

    }


    modal.classList.add("show");


    console.log(
        "Student modal opened"
    );

}


// ==========================================
// CLOSE MODAL
// ==========================================

function closeStudentModal() {

    const modal =
        document.getElementById("studentModal");

    if (modal) {

        modal.classList.remove("show");

    }

}


// ==========================================
// SAVE STUDENT
// ==========================================

async function saveStudent(event) {

    event.preventDefault();


    const studentId =
        document.getElementById("studentId").value;


    const student = {

        name:
            document.getElementById("name").value.trim(),

        age:
            Number(
                document.getElementById("age").value
            ),

        gender:
            document.getElementById("gender").value,

        email:
            document.getElementById("email").value.trim(),

        course:
            document.getElementById("course").value.trim(),

        year:
            Number(
                document.getElementById("year").value
            ),

        phone:
            document.getElementById("phone").value.trim()

    };


    try {

        let response;


        // UPDATE

        if (studentId) {

            response =
                await fetch(
                    `/students/${studentId}`,
                    {
                        method: "PUT",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(student)
                    }
                );

        }

        // CREATE

        else {

            response =
                await fetch(
                    "/students/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(student)
                    }
                );

        }


        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(error);

        }


        closeStudentModal();

        await loadStudents();


        alert(
            studentId
                ? "Student updated successfully!"
                : "Student added successfully!"
        );


    } catch (error) {

        console.error(
            "Error saving student:",
            error
        );


        alert(
            "Failed to save student.\n\n" +
            error.message
        );

    }

}


// ==========================================
// EDIT STUDENT
// ==========================================

function editStudent(id) {

    const student =
        students.find(
            student => student.id === id
        );


    if (!student) {

        return;

    }


    editingStudentId = id;


    document.getElementById("studentId").value =
        student.id;

    document.getElementById("name").value =
        student.name;

    document.getElementById("age").value =
        student.age;

    document.getElementById("gender").value =
        student.gender;

    document.getElementById("email").value =
        student.email;

    document.getElementById("course").value =
        student.course;

    document.getElementById("year").value =
        student.year;

    document.getElementById("phone").value =
        student.phone;


    document.getElementById("modalTitle")
        .textContent =
        "✏️ Edit Student";


    document
        .getElementById("studentModal")
        .classList.add("show");

}


// ==========================================
// DELETE STUDENT
// ==========================================

async function deleteStudent(id) {

    if (
        !confirm(
            "Are you sure you want to delete this student?"
        )
    ) {

        return;

    }


    try {

        const response =
            await fetch(
                `/students/${id}`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {

            throw new Error(
                "Failed to delete student"
            );

        }


        await loadStudents();


        alert(
            "Student deleted successfully!"
        );


    } catch (error) {

        console.error(error);


        alert(
            "Failed to delete student."
        );

    }

}


// ==========================================
// SEARCH STUDENTS
// ==========================================

function searchStudents() {

    const input =
        document.getElementById("searchInput");


    if (!input) return;


    const query =
        input.value.toLowerCase().trim();


    const filtered =
        students.filter(student => {

            return (

                String(student.id)
                    .includes(query)

                ||

                student.name
                    .toLowerCase()
                    .includes(query)

                ||

                student.email
                    .toLowerCase()
                    .includes(query)

                ||

                student.course
                    .toLowerCase()
                    .includes(query)

                ||

                student.gender
                    .toLowerCase()
                    .includes(query)

            );

        });


    displayStudents(filtered);

}


// ==========================================
// AI CHAT
// ==========================================

async function sendMessage() {

    const input =
        document.getElementById("chatInput");

    const messages =
        document.getElementById("chatMessages");


    if (!input || !messages) {

        return;

    }


    const message =
        input.value.trim();


    if (!message) {

        return;

    }


    // ======================================
    // SHOW USER MESSAGE
    // ======================================

    messages.innerHTML += `
        <div class="message user-message">

            <div class="message-content">
                <p>${escapeHtml(message)}</p>
            </div>

        </div>
    `;


    input.value = "";


    // ======================================
    // LOADING MESSAGE
    // ======================================

    const loadingId =
        "ai-loading-" + Date.now();


    messages.innerHTML += `
        <div
            class="message ai-message"
            id="${loadingId}">

            <div class="message-avatar">
                🤖
            </div>

            <div class="message-content">

                <p>
                    Thinking... ⏳
                </p>

            </div>

        </div>
    `;


    messages.scrollTop =
        messages.scrollHeight;


    // ======================================
    // CALL FASTAPI
    // ======================================

    try {

        const response =
            await fetch(
                "/chat/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            message: message
                        })
                }
            );


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );

        }


        const data =
            await response.json();


        // ==================================
        // REMOVE LOADING
        // ==================================

        const loading =
            document.getElementById(
                loadingId
            );


        if (loading) {

            loading.remove();

        }


        // ==================================
        // AI RESPONSE
        // ==================================

        const aiResponse =
            data.response ||
            "No response received.";


        const formattedResponse =
            escapeHtml(aiResponse)
                .replace(/\n/g, "<br>");


        messages.innerHTML += `
            <div class="message ai-message">

                <div class="message-avatar">
                    🤖
                </div>

                <div class="message-content">

                    <p>
                        ${formattedResponse}
                    </p>

                </div>

            </div>
        `;


    } catch (error) {

        console.error(
            "AI Chat Error:",
            error
        );


        const loading =
            document.getElementById(
                loadingId
            );


        if (loading) {

            loading.remove();

        }


        messages.innerHTML += `
            <div class="message ai-message">

                <div class="message-avatar">
                    🤖
                </div>

                <div class="message-content">

                    <p>
                        ❌ Unable to connect to AI.
                    </p>

                    <small>
                        ${escapeHtml(
                            error.message
                        )}
                    </small>

                </div>

            </div>
        `;

    }


    messages.scrollTop =
        messages.scrollHeight;

}


// ==========================================
// HTML ESCAPE
// ==========================================

function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent =
        String(text);

    return div.innerHTML;

}


// ==========================================
// CHAT ENTER KEY
// ==========================================

function handleChatKey(event) {

    if (event.key === "Enter") {

        sendMessage();

    }

}


// ==========================================
// PAGE LOAD
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "Student Database UI loaded"
        );


        // ======================================
        // ADD STUDENT BUTTONS
        // ======================================

        document
            .querySelectorAll(
                ".add-student-btn"
            )
            .forEach(button => {

                button.addEventListener(
                    "click",
                    openStudentModal
                );

            });


        // ======================================
        // STUDENT FORM
        // ======================================

        const form =
            document.getElementById(
                "studentForm"
            );


        if (form) {

            form.addEventListener(
                "submit",
                saveStudent
            );

        }


        // ======================================
        // LOAD STUDENTS
        // ======================================

        loadStudents();

    }
);