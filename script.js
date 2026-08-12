// --- 1. WISHES DATA ---
const wishes = [
  // 1. Merged Wish (Both of Us)
  "Happy Birthday, Sky! 🎉✨<br><br>Jia and I are sending you the absolute biggest birthday wishes today! We hope your day is filled with good vibes, lots of laughs, and all your favorite things.<br><br>May this next year bring you endless happiness, amazing adventures, and major success in everything you do. You deserve the absolute best day ever—enjoy every single second of it! 🎂🥳🎈",

  // 2. Your Wish
  "Happy Birthday, Sky! 🎈✨<br><br>I wanted to send a huge birthday wish your way! I hope today is as incredible, bright, and full of energy as you are.<br><br>Thank you for being such an awesome person to have in my life. I’m so grateful for all the fun moments we’ve shared, and I’m hyped for everything this next year has in store for you. May this year bring you huge wins, endless happiness, and all the success you’ve been working for.<br><br>Have the absolute best day celebrating—you deserve all of it and more! 🎂🥳🚀",

  // 3. Jia's Wish (RESERVED SPACE)
  "`Hey... I know we ain't talking anymore I wish we could. But god actually decided different paths for us now. But that doesn't mean that we'll NEVER be together again.<br>
Maybe one day we'll still meet again even after all the circumstances and difficulties, I know we'll meet again.<br>
I know there are still a lot of misunderstandings between us now, a lot of fights that happened in the past, our family not agreeing for us to be friends anymore, I know it's hard.<br>
But can I ask you a few things?<br><br>

If I was in trouble, will you be the first to be there for me even if I was badly wrong?<br>
Who would you want to be there for you when the same happens?<br>
Would you be my best friend forever even after the distance and misunderstandings?<br>
Would you have love for me even after I'm not here in this world anymore?<br>
Would you want to be my best friend even after I change or would you actually like the old me instead?<br>
Do you still think of me everyday like I miss you? Would you do it forever?<br>
What would you do?<br>
Would you still love me when I'm no longer young and beautiful???<br>
Because... I know you will, I know will, I know that you WILL.<br>
Remember. If you give me reasons to believe that you'll do the same for me. And I would do it for YOU!<br><br>

So tell me... how do you plan to spend your day today? Would you like me to be part of your day too?<br>
I know this one's long... but not long enough to express my love for you.<br><br>

I know I always say the same things everytime. But how do I let you know that's what I actually mean, that's how I actually feel for you?<br>
Well, even if you don't know anything about it, atleast I want you to remember one thing, even if I act cold and distant, you'll see the un-wanting-ness in my eyes to do that.<br>
Even if I avoid my eyes to meet yours, they'll still end up landing on you.<br><br>

Even if I can't show my love for you now through this distance, do you still know how much I love you?<br><br>

Happy birthday, meri jaan. Spend it like it's gold, cuz you are even more than a diamond to me. You're my everything.<br><br>

Words can't express the love I have for you. Not even actions could. But would you realize how much of it is there just by looking me dead in my eye?<br><br>

If I asked you to hold my hand and fly up to the sky, would you give me your hand?<br><br>

Now, have the best time of your life on this most special occasion. Do it for me if not yourself, would you?<br><br>

I'll have to end this text here even though there's a hundred things more to say. But I know your time is expensive, so I'll let you live. So, let's just save those talks for later, kay?<br><br>

Thank you for showing me things in life.<br>
Sorry for the things I put you through. <br>

But... let's end it with love instead of regret now, shall we?<br> 

I love you, mi' lady.<br>

Even though not the way you wanted, yes. But atleast my love ain't short or fake. It'll always be real.<br>",
];

// --- 2. TAB SWITCHER FUNCTION ---
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

// --- 3. LIVE COUNTDOWN TIMER (FOR AUGUST 13TH) ---
function startCountdown() {
  const timerElement = document.getElementById("timer");

  function updateTimer() {
    const now = new Date();
    let currentYear = now.getFullYear();
    
    // Set target date to August 13th
    let targetDate = new Date(currentYear, 7, 13, 0, 0, 0); // Month 7 = August (0-indexed)

    // If Aug 13th has already passed this year, set target to next year
    if (now > targetDate && now.getDate() !== 13) {
      targetDate = new Date(currentYear + 1, 7, 13, 0, 0, 0);
    }

    // Check if TODAY is August 13th
    if (now.getMonth() === 7 && now.getDate() === 13) {
      timerElement.innerHTML = "🎉 IT'S SKY'S BIRTHDAY TODAY! 🥳";
      return;
    }

    const diff = targetDate - now;

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const minutes = Math.floor((diff / (1000 * 60)) % 60);
    const seconds = Math.floor((diff / 1000) % 60);

    timerElement.innerHTML = `${days}d : ${hours}h : ${minutes}m : ${seconds}s`;
  }

  updateTimer();
  setInterval(updateTimer, 1000);
}

// --- 4. CONFETTI CANNON ---
function launchConfetti() {
  if (typeof confetti === 'function') {
    confetti({
      particleCount: 120,
      spread: 80,
      origin: { y: 0.6 }
    });
  }
}

// --- 5. BLOW OUT CANDLE INTERACTION ---
let candleBlown = false;

function blowCandle() {
  if (candleBlown) return;

  const flame = document.getElementById("flame");
  const text = document.getElementById("candleText");

  flame.style.display = "none"; // Extinguish the flame
  candleBlown = true;

  text.innerHTML = "✨ Your wish has been made! 🎉";
  text.style.color = "#fdcb6e";

  // Trigger celebration confetti
  launchConfetti();
}

// --- 6. BACKGROUND MUSIC TOGGLE ---
function toggleMusic() {
  const audio = document.getElementById('bgMusic');
  const btn = document.getElementById('musicBtn');

  if (audio.paused) {
    audio.play();
    btn.innerText = "⏸️ Pause Music";
  } else {
    audio.pause();
    btn.innerText = "🎵 Play Music";
  }
}

// --- 7. INITIALIZE PAGE & PARTICLES ---
document.addEventListener("DOMContentLoaded", () => {
  // Load default merged wish
  document.getElementById("wishDisplay").innerHTML = wishes[0];

  // Start live timer
  startCountdown();

  // Floating background particles
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
});
