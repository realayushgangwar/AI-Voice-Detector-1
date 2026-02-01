
document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize WaveSurfer with a "Neon" look
    const wavesurfer = WaveSurfer.create({
        container: '#waveform',
        waveColor: '#334155',      // Muted Slate
        progressColor: '#818cf8',  // Glowing Indigo
        cursorColor: '#818cf8',
        height: 80,
        barWidth: 3,
        barGap: 4,
        barRadius: 20,
        responsive: true,
    });

    const dropZone = document.getElementById('drop-zone');
    const audioInput = document.getElementById('audio-input');
    const playbackContainer = document.getElementById('playback-container');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsDisplay = document.getElementById('results-display');
    const playBtn = document.getElementById('play-btn');

    // --- 1. File Handling Logic ---
    dropZone.onclick = () => audioInput.click();

    audioInput.onchange = (e) => {
        const file = e.target.files[0];
        if (file) handleAudioUpload(file);
    };

    function handleAudioUpload(file) {
        // Show the playback UI
        playbackContainer.classList.remove('hidden');
        document.getElementById('file-name').innerText = file.name;
        
        // Load waveform
        const url = URL.createObjectURL(file);
        wavesurfer.load(url);

        // Convert to Base64 for the Level 2 API
        const reader = new FileReader();
        reader.onloadend = () => {
            window.audioBase64 = reader.result.split(',')[1];
            console.log("Audio encoded to Base64. Ready for API submission.");
        };
        reader.readAsDataURL(file);

        // Smooth scroll to playback
        playbackContainer.scrollIntoView({ behavior: 'smooth' });
    }

    // --- 2. Playback Control ---
    playBtn.onclick = () => {
        wavesurfer.playPause();
        playBtn.innerHTML = wavesurfer.isPlaying() ? 
            '<span class="pause-icon">||</span> Pause' : 
            '<span class="play-icon">▶</span> Play';
    };

    // --- 3. The "Scanning" Intelligence ---
    analyzeBtn.onclick = () => {
        // Visual state: Scanning
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<span class="loader"></span> Analyzing Audio...';
        
        // Inject the Scan Line (from your CSS)
        const scanLine = document.createElement('div');
        scanLine.className = 'scan-line';
        document.getElementById('waveform').appendChild(scanLine);

        // Simulate AI Thinking Time
        setTimeout(() => {
            scanLine.remove();
            displayResults();
            analyzeBtn.disabled = false;
            analyzeBtn.innerText = "Verify Authenticity";
        }, 3000);
    };

    // --- 4. Dynamic Results Presentation ---
    function displayResults() {
        resultsDisplay.classList.remove('hidden');
        
        // This data will eventually come from your Python/Node API
        const mockResponse = {
            lang: "Telugu",
            score: 97.8,
            isAI: true,
            details: "Neural vocoder artifacts detected. Spectral flux distribution is too consistent for human vocal cords. Lack of physiological micro-jitters in the 4kHz range."
        };

        const label = document.getElementById('classification-label');
        const badge = document.getElementById('language-badge');
        const scoreVal = document.getElementById('score-value');
        const terminalText = document.getElementById('explanation-text');

        // Apply dynamic styles based on result
        label.innerText = mockResponse.isAI ? "AI-GENERATED VOICE" : "HUMAN VOICE DETECTED";
        label.style.color = mockResponse.isAI ? "#fb7185" : "#34d399";
        badge.innerText = `${mockResponse.lang} Detected`;
        
        // Animate the score counting up
        animateScore(scoreVal, mockResponse.score);

        // Typewriter effect for the terminal breakdown
        typeWriter(terminalText, `> [SYSTEM_REPORT]: ${mockResponse.details}`);

        resultsDisplay.scrollIntoView({ behavior: 'smooth' });
    }

    // Helper: Count up animation
    function animateScore(element, target) {
        let count = 0;
        const speed = 2000 / target;
        const timer = setInterval(() => {
            count += 0.5;
            element.innerText = count.toFixed(1);
            if (count >= target) {
                element.innerText = target;
                clearInterval(timer);
            }
        }, 10);
    }

    // Helper: Typewriter effect
    function typeWriter(element, text, i = 0) {
        if (i === 0) element.innerHTML = '';
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            setTimeout(() => typeWriter(element, text, i + 1), 20);
        }
    }
});
