// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getDatabase } from "firebase/database";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyB70vC2OmlykAWcbt6DBlC5UM8CnBne-rM",
  authDomain: "v2x-app.firebaseapp.com",
  databaseURL: "https://v2x-app-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "v2x-app",
  storageBucket: "v2x-app.appspot.com",
  messagingSenderId: "290272227732",
  appId: "1:290272227732:web:d2dd21091eed1697a39f81",
  measurementId: "G-JTT78NQD67"
};

// Initialize Firebase
export const FIREBASE_APP = initializeApp(firebaseConfig);
export const FIREBASE_AUTH = getAuth(FIREBASE_APP)
export const FIREBASE_DB = getDatabase(FIREBASE_APP)
