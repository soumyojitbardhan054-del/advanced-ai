const wishes = [
  // 1. Merged Wish
  "Happy Birthday, Sky! 🎉✨<br><br>Jia and I are sending you the absolute biggest birthday wishes today! We hope your day is filled with good vibes, lots of laughs, and all your favorite things.<br><br>May this next year bring you endless happiness, amazing adventures, and major success in everything you do. You deserve the absolute best day ever—enjoy every single second of it! 🎂🥳🎈",

  // 2. Your Individual Wish
  "Happy Birthday, Sky! 🎈✨<br><br>I wanted to send a huge birthday wish your way! I hope today is as incredible, bright, and full of energy as you are.<br><br>Thank you for being such an awesome person to have in my life. I’m so grateful for all the fun moments we’ve shared, and I’m hyped for everything this next year has in store for you. May this year bring you huge wins, endless happiness, and all the success you’ve been working for.<br><br>Have the absolute best day celebrating—you deserve all of it and more! 🎂🥳🚀",

  // 3. Jia's Wish (RESERVED SPACE)
  "<i>Jia's special wish is incoming... Stay tuned! 💖✨</i>"
];

function showWish(index, btnElement) {
  const display = document.getElementById("wishDisplay");
  
  document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
  btnElement.classList.add("active");

  display.style.opacity = 0;
  setTimeout(() => {
    display.innerHTML = wishes[index];
    display.style.opacity = 1;
  }, 200);
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("wishDisplay").innerHTML = wishes[0];
});

// Particle Animation
for (let i = 0; i < 35; i++) {
  const particle = document.createElement("div");
  particle.classList.add("particle");
  
  const size = Math.random() * 12 + 6;
  particle.style.width = size + "px";
  particle.style.height = size + "px";
  particle.style.left = Math.random() * 100 + "vw";
  particle.style.animationDuration = (Math.random() * 4 + 4) + "s";
  particle.style.animationDelay = Math.random() * 3 + "s";
  
  const colors = ["#ff7675", "#fdcb6e", "#00b894", "#74b9ff", "#a29bfe", "#fd79a8"];
  particle.style.background = colors[Math.floor(Math.random() * colors.length)];
  
  document.body.appendChild(particle);
}
