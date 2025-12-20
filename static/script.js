// Test AI Connection
document.getElementById('testAI').addEventListener('click', async function() {
    const resultDiv = document.getElementById('testResult');
    resultDiv.textContent = 'Testing AI connection...';
    resultDiv.className = '';
    resultDiv.style.display = 'block';
    
    try {
        const response = await fetch('/test_ai');
        const data = await response.json();
        
        if (data.success) {
            resultDiv.textContent = '✅ ' + data.response;
            resultDiv.className = 'success';
        } else {
            resultDiv.textContent = '❌ Error: ' + data.error;
            resultDiv.className = 'error';
        }
    } catch (error) {
        resultDiv.textContent = '❌ Failed to connect: ' + error.message;
        resultDiv.className = 'error';
    }
});

// Add Note with AI Summary
document.getElementById('addNote').addEventListener('click', async function() {
    const noteInput = document.getElementById('noteInput');
    const noteText = noteInput.value.trim();
    const resultDiv = document.getElementById('addResult');
    
    if (!noteText) {
        resultDiv.textContent = '⚠️ Please enter a note';
        resultDiv.className = 'error';
        resultDiv.style.display = 'block';
        return;
    }
    
    resultDiv.textContent = '🤖 Adding note and generating AI summary...';
    resultDiv.className = 'loading';
    resultDiv.style.display = 'block';
    
    try {
        const response = await fetch('/add_note', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ note: noteText })
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.textContent = '✅ ' + data.message;
            resultDiv.className = 'success';
            noteInput.value = ''; // Clear input
            
            // Auto-reload notes
            setTimeout(() => {
                document.getElementById('loadNotes').click();
            }, 500);
        } else {
            resultDiv.textContent = '❌ Error: ' + data.error;
            resultDiv.className = 'error';
        }
    } catch (error) {
        resultDiv.textContent = '❌ Failed to add note: ' + error.message;
        resultDiv.className = 'error';
    }
});

// Generate AI Insights
document.getElementById('getInsights').addEventListener('click', async function() {
    const resultDiv = document.getElementById('insightsResult');
    resultDiv.innerHTML = '<p class="loading">🤖 AI is analyzing your learning patterns...</p>';
    
    try {
        const response = await fetch('/get_insights');
        const data = await response.json();
        
        if (data.success) {
            resultDiv.innerHTML = `
                <div class="insights-box">
                    <h3 style="color: #ff9800; margin-bottom: 15px;">📊 Your Learning Insights (${data.total_notes} notes analyzed)</h3>
                    <div>${data.insights}</div>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `<div class="error">${data.message}</div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="error">❌ Failed to generate insights: ${error.message}</div>`;
    }
});

// Load Notes
document.getElementById('loadNotes').addEventListener('click', async function() {
    const notesList = document.getElementById('notesList');
    notesList.innerHTML = '<p style="text-align: center; color: #666;">Loading notes...</p>';
    
    try {
        const response = await fetch('/get_notes');
        const data = await response.json();
        
        if (data.notes.length === 0) {
            notesList.innerHTML = '<div class="empty-state">📝 No notes yet. Start adding your learnings!</div>';
            return;
        }
        
        // Display notes (newest first)
        notesList.innerHTML = '';
        data.notes.reverse().forEach(note => {
            const noteDiv = document.createElement('div');
            noteDiv.className = 'note-item';
            
            let summaryHTML = '';
            if (note.summary) {
                summaryHTML = `<div class="note-summary">🤖 AI Summary: ${note.summary}</div>`;
            }
            
            noteDiv.innerHTML = `
                <div class="note-header">
                    <span>📅 ${note.timestamp}</span>
                    <span>Note #${note.id}</span>
                </div>
                <div class="note-text">${note.text}</div>
                ${summaryHTML}
            `;
            notesList.appendChild(noteDiv);
        });
    } catch (error) {
        notesList.innerHTML = `<div class="error">❌ Failed to load notes: ${error.message}</div>`;
    }
});

// Load notes on page load
window.addEventListener('load', function() {
    document.getElementById('loadNotes').click();
});