// Test script to simulate frontend behavior
const API_BASE_URL = 'http://localhost:8000';

async function testUserFlow() {
  console.log('Testing user registration...');
  
  // Register a new user
  const registerResponse = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: 'testuser@example.com',
      password: 'password123',
      full_name: 'Test User'
    })
  });
  
  const registerData = await registerResponse.json();
  console.log('Registration response:', registerData);
  
  if (!registerResponse.ok) {
    console.error('Registration failed:', registerData);
    return;
  }
  
  const token = registerData.access_token;
  console.log('Received token:', token.substring(0, 20) + '...');
  
  // Create a task with the token
  console.log('\nCreating a task...');
  const taskResponse = await fetch(`${API_BASE_URL}/api/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      title: 'Test Task from Frontend',
      description: 'This task was created to test the frontend flow'
    })
  });
  
  const taskData = await taskResponse.json();
  console.log('Task creation response:', taskData);
  
  if (!taskResponse.ok) {
    console.error('Task creation failed:', taskData);
    return;
  }
  
  // Get tasks with the token
  console.log('\nGetting tasks...');
  const getTasksResponse = await fetch(`${API_BASE_URL}/api/tasks`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const getTasksData = await getTasksResponse.json();
  console.log('Get tasks response:', getTasksData);
  
  if (!getTasksResponse.ok) {
    console.error('Get tasks failed:', getTasksData);
    return;
  }
  
  console.log('\nTest completed successfully!');
}

testUserFlow().catch(console.error);