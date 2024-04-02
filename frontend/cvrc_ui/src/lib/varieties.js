import { writable } from "svelte/store";

/**
 * Function to create a writable store with persistence
 * @param {string} key - The key for localStorage
 * @param {any} initialValue - The initial value of the store
 * @param {string} storeName - The name for the exported store
 */
export function persistentWritable(key, initialValue, storeName) {
  let initialValueToUse = initialValue;

  if (typeof localStorage !== 'undefined') {
    const savedValue = localStorage.getItem(key);
    initialValueToUse = savedValue !== null ? JSON.parse(savedValue) : initialValue;
  }

  const store = writable(initialValueToUse);

  if (typeof localStorage !== 'undefined') {
    // Clear localStorage on initialization to store only the most recent data
    localStorage.removeItem(key);
    
    // Subscribe to changes and update localStorage with the latest value
    store.subscribe(value => {
      localStorage.setItem(key, JSON.stringify(value));
    });
  }

  return store;
}

// Create a persistent store called "varieties" with default value as an empty object
const varieties = persistentWritable("varieties", {}, "varieties");

export default varieties;
