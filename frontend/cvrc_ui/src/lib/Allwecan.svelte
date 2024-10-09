<script>
    let showModal = false;
  
    function toggleModal() {
      showModal = !showModal;
    }
  </script>
  
  <main>
    <button on:click={toggleModal}>Open Modal</button>
  
    {#if showModal}
      <div class="modal">
        <div class="modal-content">
          <span class="close" on:click={toggleModal}>&times;</span>
          <h2>Modal Title</h2>
          <p>Modal content goes here...</p>
        </div>
      </div>
    {/if}
  </main>
  
  <style>
    .modal {
      position: fixed;
      z-index: 1;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0, 0, 0, 0.4);
    }
  
    .modal-content {
      background-color: #fefefe;
      margin: 15% auto;
      padding: 20px;
      border: 1px solid #888;
      width: 30%;
    }
  
    .close {
      color: #aaa;
      float: right;
      font-size: 28px;
      font-weight: bold;
    }
  
    .close:hover,
    .close:focus {
      color: black;
      text-decoration: none;
      cursor: pointer;
    }
  </style>