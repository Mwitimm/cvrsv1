import { writable } from 'svelte/store';

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
    store.subscribe(value => {
      localStorage.setItem(key, JSON.stringify(value));
    });
  }

  return {
    subscribe: store.subscribe,
    set: (/** @type {any} */ value) => {
      store.set(value); // Set the store's value directly to the new data
    }
  };
}

// Create a persistent store called "specific" with default value as an empty object
const specific = persistentWritable("specific", {}, "specific");

export default specific;
