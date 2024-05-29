document.getElementById('search-btn').addEventListener('click', async () => {
    const instagramUsername = document.getElementById('instagram-username').value;
    const instagramPassword = document.getElementById('instagram-password').value;
    const targetUsername = document.getElementById('target-username').value;
    const usersList = document.getElementById('users-list');
    usersList.innerHTML = '';

    if (!instagramUsername || !instagramPassword || !targetUsername) {
        alert('Please enter all required fields.');
        return;
    }

    const response = await fetch('/api/engaged_users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            instagram_username: instagramUsername,
            instagram_password: instagramPassword,
            target_username: targetUsername
        })
    });

    if (response.ok) {
        const engagedUsers = await response.json();
        engagedUsers.forEach(([user, count]) => {
            const li = document.createElement('li');
            li.textContent = `${user}: ${count} engagements`;
            usersList.appendChild(li);
        });
    } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
    }
});
