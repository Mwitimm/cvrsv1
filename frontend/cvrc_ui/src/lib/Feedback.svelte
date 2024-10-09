<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import selectedFeedback from "$lib/feedback.js";
    import login from "$lib/login.js";
    import toast, { Toaster } from 'svelte-french-toast';
  
    let selectedVariety = {};
    let userInfo = {};
    let feedbackText = '';
  
    onMount(async () => {
      selectedFeedback.subscribe(crop => {
        selectedVariety = crop;
      });
  
      login.subscribe(values => {
        userInfo = values;
      });
    });

  
    async function createFeedback() {
        try {
          const feedback = {
            reccomenadtion_id: selectedVariety.variety_id,
            user_id: userInfo.user_id,
            feedback_text: feedbackText
          };
      
          const res = await fetch("http://localhost:8080/feedback", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(feedback)
          });
      
          if (!res.ok) {
            throw new Error('Failed to create feedback');
            toast.error("Failed to create feedback")
          }
      
          // Show success toast
          toast.success("Feedback received");
      
          // Redirect to dashboard after successful feedback
          goto("/dashboard");
        } catch (error) {
          console.error('Error:', error);
          // Handle error if needed
        }
      }
  </script>

  <Toaster/>

  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="feedback-form">
      <h1 class="mb-4">Feedback</h1>
      <form class="row g-3" on:submit={createFeedback}>
        <div class="col-md-12">
          <div class="mb-3">
            <label for="location" class="form-label">Feedback</label>
            <input type="text" class="form-control" id="location" placeholder="Enter text" bind:value={feedbackText}>
          </div>
        </div>
        <div class="col-md-12 d-grid">
          <button type="submit" class="btn btn-success submit-button">
            Submit
          </button>
        </div>
      </form>
    </div>
  </div>

  <style>
    .feedback-form {
        max-width: 400px;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 10px;
        background-color: #f8f9fa;
      }
      
      .submit-button {
        background-color: #28a745; /* Green */
        border-color: #28a745; /* Green */
      }
      
      .submit-button:hover {
        background-color: #218838; /* Darker green */
        border-color: #218838; /* Darker green */
      }
      
  </style>

  



