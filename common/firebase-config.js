import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyBFthWAYk972aNTPwktUMXkU3uEkjclPkA",
  authDomain: "cosc432-4f209.firebaseapp.com",
  projectId: "cosc432-4f209",
  storageBucket: "cosc432-4f209.firebasestorage.app",
  messagingSenderId: "710164407822",
  appId: "1:710164407822:web:c36070bc368cd4d05ebe5f",
  measurementId: "G-GMVSQFDZPR"
};

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();
export { auth };
