<script>

    import { goto } from '$app/navigation';
    function getStarted() {
       goto("/signup")
    }
  </script>



    <div class="no-prediction-container">
      <div class="no-prediction-content">
        <h2>Start</h2>
        <p>
          Welcome to our agricultural platform! We're excited to help you start a new project.
          Please provide some information about your land  and we'll recommend the best crops for you to grow.
        </p>
        <button class="start-button" on:click={getStarted}>Get Started</button>
      </div>
    </div>

  

  
  <style>
    .no-prediction-container {
      background-image: url('https://source.unsplash.com/random/1920x1080/?farm,field');
      background-size: cover;
      background-position: center;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #f5f5f5;
    }
  
    .no-prediction-content {
      text-align: center;
      max-width: 500px;
      padding: 2rem;
      background-color: rgba(255, 255, 255, 0.9); /* Adjusted background color for better readability */
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
  
    h2 {
      font-size: 2rem;
      color: #4d7c0f;
      margin-bottom: 1.5rem; /* Increased margin for better separation */
    }
  
    p {
      font-size: 1.2rem;
      color: #333;
      margin-bottom: 2rem;
    }
  
    .start-button {
      background-color: #4d7c0f;
      color: #fff;
      border: none;
      padding: 0.8rem 1.6rem;
      font-size: 1.2rem;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
  
    .start-button:hover {
      background-color: #3b6109;
    }
  </style>
  