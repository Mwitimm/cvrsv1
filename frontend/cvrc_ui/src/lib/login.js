import { writable } from 'svelte/store';

// Function to create a writable store with persistence
/**
 * @param {string} key
 * @param {any} initialValue
 */
function persistentWritable(key, initialValue) {
  let initialValueToUse = initialValue;

  if (typeof localStorage !== 'undefined') {
    const savedValue = localStorage.getItem(key);
    initialValueToUse = savedValue !== null ? JSON.parse(savedValue) : initialValue;
  }

  const store = writable(initialValueToUse);

  if (typeof localStorage !== 'undefined') {
    store.subscribe(value => {
      localStorage.setItem(key, JSON.stringify(value));
    });
  }

  return store;
}

// Create a persistent store called "login" with default value false and user info null
const login = persistentWritable("login", { isLoggedIn: false, userInfo: null });

export default login;
