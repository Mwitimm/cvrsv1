<script>
    import { readable, writable } from 'svelte/store';
  
    export let duration = 3000; // Default duration for the notification
    export const notification = writable(null);
  
    // Types of notifications
    export const NOTIFICATION_TYPES = {
      SUCCESS: 'success',
      ERROR: 'error'
    };
  
    // Function to show the notification
    export function showNotification(type, message) {
      notification.set({ type, message });
      setTimeout(() => notification.set(null), duration);
    }
  </script>

  {#if $notification !== null}
  <div class="notification" class:success="{$notification.type === NOTIFICATION_TYPES.SUCCESS}" class:error="{$notification.type !== NOTIFICATION_TYPES.SUCCESS}">
  {$notification.message}
</div>
{/if}


  
  <style>
    .notification {
      position: fixed;
      bottom: 20px;
      right: 20px;
      padding: 10px;
      border-radius: 5px;
      color: #fff;
      z-index: 9999;
    }
  
    .success {
      background-color: green;
    }
  
    .error {
      background-color: red;
    }
  </style>
  