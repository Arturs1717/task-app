const API = "http://127.0.0.1:5000/tasks";

async function loadTasks() {
    const res = await fetch(API);
    const data = await res.json();

    const list = document.getElementById("list");
    list.innerHTML = "";

    data.forEach(task => {
        const li = document.createElement("li");
        li.innerHTML = `
            ${task.name} - ${task.description}
            <button onclick="deleteTask(${task.id})">Delete</button>
        `;
        list.appendChild(li);
    });
}

async function addTask() {
    const name = document.getElementById("name").value;
    const desc = document.getElementById("desc").value;

    await fetch(API, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            description: desc
        })
    });

    loadTasks();
}

async function deleteTask(id) {
    await fetch(API + "/" + id, {
        method: "DELETE"
    });

    loadTasks();
}

loadTasks();