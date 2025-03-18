const questions = [
    {
      question: "At which accelerating voltage does an FEI Talos F200X typically operate?",
      mediaType: "image",
      mediaSrc: "media/ewald_sphere.pdf",
      options: ["100 kV", "200 kV", "300 kV"],
      correct: 1,
      feedback: "FEI Talos F200X typically operates at 200 kV."
    },
    {
      question: "What does the Ewald sphere help explain in electron diffraction?",
      media: {type: "image", src: "ewald_sphere.pdf"},
      options: [
        "Resolution limit of microscopes",
        "Geometric construction to visualize diffraction conditions",
        "Image resolution limitations"
      ],
      correct: 1,
      feedback: "Correct! The Ewald sphere helps visualize diffraction conditions."
    },
    {
      question: "Identify this diffraction pattern type:",
      media: {type: "video", src: "diffraction.mp4"},
      options: ["Ring pattern (polycrystalline)", "Single crystal spot pattern", "Amorphous halo"],
      correct: 0,
      feedback: "Correct! Ring patterns indicate polycrystalline materials."
    }
  ];
  
  let currentQuestion = 0;
  
  function showQuestion(index) {
    const q = questions[index];
    document.getElementById('feedback-container').innerHTML = "";
    document.getElementById('next-btn').classList.add('hidden');
  
    const questionText = `<h3>Question ${index+1} of ${questions.length}</h3><p>${q.question}</p>`;
    document.getElementById('feedback-container').innerHTML = '';
    
    document.getElementById('options-container').innerHTML = q.options.map((opt, i) => `
      <button onclick="checkAnswer(${i}, this)">${opt}</button>
    `).join('');
  
    document.getElementById('next-btn').onclick = () => nextQuestion();
  
    const mediaDiv = document.getElementById('media-container');
    if (q.media) {
      if (q.media.type === 'image') {
        mediaDiv = `<img src="${q.media.src}" style="max-width:90%;border-radius:8px;">`;
      } else if (q.media.type === 'video') {
        mediaHtml = `<video controls style="max-width:90%;border-radius:8px;">
                       <source src="${q.media.src}" type="video/mp4">
                     Your browser doesn't support video playback.
                     </video>`;
      }
      document.getElementById('media-container').innerHTML = mediaHtml;
    } else {
      document.getElementById('feedback-container').innerHTML = '';
    }
  
    document.getElementById('next-btn').classList.add('hidden');
    document.getElementById('question').innerHTML = questionHtml;
  }
  
  function checkAnswer(selected, btn) {
    const q = questions[currentQuestion];
    let feedbackContainer = document.getElementById('feedback-container');
    document.querySelectorAll('#options-container button').forEach(btn => btn.disabled = true);
  
    if (selected === q.correct) {
      btn.classList.add('correct');
      feedbackContainer.innerHTML = `<p>✅ Correct! ${q.feedback}</p>`;
    } else {
      btn.classList.add('incorrect');
      feedbackContainer.innerHTML = `Incorrect. ${q.feedback}`;
    }
    document.getElementById('next-btn').classList.remove('hidden');
  }
  
  document.getElementById('next-btn').onclick = () => {
    currentQuestion++;
    if (currentQuestion < questions.length) {
      displayQuestion(currentQuestion);
    } else {
      document.getElementById('question').innerHTML = `<h3>Quiz Completed!</h3>`;
      document.getElementById('options-container').innerHTML = '';
      document.getElementById('feedback-container').innerHTML = "🎉 You've completed the quiz!";
      document.getElementById('next-btn').classList.add('hidden');
    }
  };
  
  function displayQuestion(index) {
    const q = questions[index];
    document.getElementById('feedback-container').innerHTML = '';
    let mediaHtml = '';
    if (q.media) {
      if (q.media.type === 'image') {
        mediaHtml = `<img src="media/${q.media.src}" alt="question image">`;
      } else if (q.media.type === 'video') {
        mediaHtml = `<video controls width="90%">
                       <source src="${'diffraction.mp4'}" type="video/mp4">
                     </video>`;
      }
    }
    document.getElementById('question').innerHTML = `<h3>Question ${index + 1}</h3><p>${q.question}</p>${mediaHtml}`;
  
    document.getElementById('options-container').innerHTML = q.options.map((opt, i) => 
      `<button onclick="checkAnswer(${i}, this)">${opt}</button>`
    ).join('');
    
    document.getElementById('next-btn').classList.add('hidden');
  }
  
  // Initialize first question
  document.body.onload = () => displayQuestion(currentQuestion);
  