<h2>🧠 Model Architecture</h2>

<p>
The proposed system combines <strong>MobileNetV2</strong> for spatial feature extraction with a
<strong>Bidirectional LSTM (BiLSTM)</strong> for learning temporal patterns across video frames.
</p>

<table>
  <tr>
    <th>Stage</th>
    <th>Component</th>
    <th>Purpose</th>
  </tr>
  <tr>
    <td>1</td>
    <td><strong>Video Input</strong></td>
    <td>Accepts an uploaded surveillance video.</td>
  </tr>
  <tr>
    <td>2</td>
    <td><strong>Frame Extraction</strong></td>
    <td>Extracts 16 equally spaced frames from the video.</td>
  </tr>
  <tr>
    <td>3</td>
    <td><strong>Preprocessing</strong></td>
    <td>Converts frames to RGB, resizes them to 224 × 224, and applies MobileNetV2 preprocessing.</td>
  </tr>
  <tr>
    <td>4</td>
    <td><strong>TimeDistributed + MobileNetV2</strong></td>
    <td>Extracts spatial features from each frame using transfer learning.</td>
  </tr>
  <tr>
    <td>5</td>
    <td><strong>Bidirectional LSTM</strong></td>
    <td>Learn temporal relationships between consecutive video frames.</td>
  </tr>
  <tr>
    <td>6</td>
    <td><strong>Dense Layers</strong></td>
    <td>Process the learned features for classification.</td>
  </tr>
  <tr>
    <td>7</td>
    <td><strong>Sigmoid Output</strong></td>
    <td>Produces the probability of the video being violent.</td>
  </tr>
</table>

<br>

<p align="center">
  <strong>Input Shape:</strong> <code>(16, 224, 224, 3)</code>
  &nbsp;&nbsp;→&nbsp;&nbsp;
  <strong>Output Shape:</strong> <code>(1)</code>
</p>

<h3>Architecture Flow</h3>

<p align="center">
  <code>Video</code>
  ↓
  <code>16 Frames</code>
  ↓
  <code>224 × 224 × 3</code>
  ↓
  <code>TimeDistributed(MobileNetV2)</code>
  ↓
  <code>Bidirectional LSTM</code>
  ↓
  <code>Dense Layers</code>
  ↓
  <code>Sigmoid</code>
  ↓
  <strong>Violence / NonViolence</strong>
</p>

<h2>🛠️ Technologies Used</h2>

<table>
  <tr>
    <th>Category</th>
    <th>Technologies</th>
  </tr>
  <tr>
    <td><strong>Programming Language</strong></td>
    <td>Python</td>
  </tr>
  <tr>
    <td><strong>Deep Learning</strong></td>
    <td>TensorFlow, Keras</td>
  </tr>
  <tr>
    <td><strong>Pretrained Model</strong></td>
    <td>MobileNetV2</td>
  </tr>
  <tr>
    <td><strong>Sequence Model</strong></td>
    <td>Bidirectional LSTM</td>
  </tr>
  <tr>
    <td><strong>Computer Vision</strong></td>
    <td>OpenCV</td>
  </tr>
  <tr>
    <td><strong>Numerical Computing</strong></td>
    <td>NumPy</td>
  </tr>
  <tr>
    <td><strong>Data Processing</strong></td>
    <td>Pandas</td>
  </tr>
  <tr>
    <td><strong>Backend</strong></td>
    <td>Flask</td>
  </tr>
  <tr>
    <td><strong>Frontend</strong></td>
    <td>HTML, CSS, JavaScript</td>
  </tr>
  <tr>
    <td><strong>Development Environment</strong></td>
    <td>Google Colab, Jupyter Notebook</td>
  </tr>
  <tr>
    <td><strong>Version Control</strong></td>
    <td>Git, GitHub</td>
  </tr>
</table>

<h2>🏋️ Model Training</h2>

<p>
The model was trained using a <strong>two-stage transfer learning approach</strong>.
</p>

<h3>Stage 1 — Frozen MobileNetV2</h3>

<p>
Initially, the pretrained MobileNetV2 feature extraction layers were kept frozen.
Only the newly added classification layers were trained. This allowed the model to
use the general visual features learned from the pretrained network.
</p>

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Sequence Length</td>
    <td>16 frames</td>
  </tr>
  <tr>
    <td>Frame Size</td>
    <td>224 × 224</td>
  </tr>
  <tr>
    <td>Learning Rate</td>
    <td>1 × 10<sup>-4</sup></td>
  </tr>
  <tr>
    <td>Frozen Training Epochs</td>
    <td>2</td>
  </tr>
</table>

<h3>Stage 2 — Fine-Tuning</h3>

<p>
For fine-tuning, the last <strong>40 layers of MobileNetV2</strong> were unfrozen.
A smaller learning rate was used so that the pretrained features could gradually
adapt to the violence detection task without significantly disturbing the useful
features already learned.
</p>

<table>
  <tr>
    <th>Parameter</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Trainable MobileNetV2 Layers</td>
    <td>Last 40 layers</td>
  </tr>
  <tr>
    <td>Learning Rate</td>
    <td>1 × 10<sup>-5</sup></td>
  </tr>
  <tr>
    <td>Fine-Tuning Epochs</td>
    <td>5</td>
  </tr>
</table>

<p>
The final fine-tuned model was selected based on validation performance and then
evaluated on a separate test set containing <strong>300 videos</strong>.
</p>

<h2>📊 Model Performance</h2>

<p>
The final model was evaluated using accuracy, precision, recall, F1-score,
and a confusion matrix.
</p>

<table>
  <tr>
    <th>Metric</th>
    <th>Frozen Model</th>
    <th>Fine-Tuned Model</th>
  </tr>
  <tr>
    <td><strong>Accuracy</strong></td>
    <td>93.00%</td>
    <td><strong>96.00%</strong></td>
  </tr>
  <tr>
    <td><strong>Precision</strong></td>
    <td>91.61%</td>
    <td><strong>97.26%</strong></td>
  </tr>
  <tr>
    <td><strong>Recall</strong></td>
    <td>94.67%</td>
    <td>94.67%</td>
  </tr>
  <tr>
    <td><strong>F1-Score</strong></td>
    <td>93.11%</td>
    <td><strong>95.95%</strong></td>
  </tr>
</table>

<h3>Final Fine-Tuned Model</h3>

<table>
  <tr>
    <th>Metric</th>
    <th>Result</th>
  </tr>
  <tr>
    <td>Accuracy</td>
    <td><strong>96.00%</strong></td>
  </tr>
  <tr>
    <td>Precision</td>
    <td><strong>97.26%</strong></td>
  </tr>
  <tr>
    <td>Recall</td>
    <td><strong>94.67%</strong></td>
  </tr>
  <tr>
    <td>F1-Score</td>
    <td><strong>95.95%</strong></td>
  </tr>
</table>

<h3>Confusion Matrix — Fine-Tuned Model</h3>

<table>
  <tr>
    <th></th>
    <th>Predicted NonViolence</th>
    <th>Predicted Violence</th>
  </tr>
  <tr>
    <th>Actual NonViolence</th>
    <td>146</td>
    <td>4</td>
  </tr>
  <tr>
    <th>Actual Violence</th>
    <td>8</td>
    <td>142</td>
  </tr>
</table>

<p>
The fine-tuned model improved the test accuracy from <strong>93%</strong> to
<strong>96%</strong> compared with the frozen model.
</p>

<h2>⚙️ Installation</h2>

<h3>1. Clone the Repository</h3>

<pre><code>git clone https://github.com/ShravaniChavhan/AI-Violence-Detection.git
cd AI-Violence-Detection</code></pre>

<h3>2. Create a Virtual Environment</h3>

<pre><code>python -m venv venv</code></pre>

<h3>3. Activate the Virtual Environment</h3>

<p><strong>Windows — Git Bash:</strong></p>

<pre><code>source venv/Scripts/activate</code></pre>

<p><strong>Windows — Command Prompt:</strong></p>

<pre><code>venv\Scripts\activate</code></pre>

<h3>4. Install Dependencies</h3>

<pre><code>pip install -r requirements.txt</code></pre>

<p>
The required Python packages are listed in
<code>requirements.txt</code>.
</p>

<h2>▶️ Running the Application</h2>

<h3>1. Activate the Virtual Environment</h3>

<pre><code>source venv/Scripts/activate</code></pre>

<h3>2. Start the Flask Application</h3>

<pre><code>python app.py</code></pre>

<p>
Once the Flask server starts, open the following address in your browser:
</p>

<p align="center">
  <a href="http://127.0.0.1:5000">
    <strong>http://127.0.0.1:5000</strong>
  </a>
</p>

<h3>3. Upload a Video</h3>

<ol>
  <li>Open the web application.</li>
  <li>Click the <strong>Choose File</strong> button.</li>
  <li>Select a supported video.</li>
  <li>Submit the video for analysis.</li>
  <li>The system extracts 16 frames from the video.</li>
  <li>The trained model performs the classification.</li>
  <li>The application displays the predicted class and confidence score.</li>
</ol>

<h3>Supported Video Formats</h3>

<p>
<code>.mp4</code> &nbsp;
<code>.avi</code> &nbsp;
<code>.mov</code> &nbsp;
<code>.mkv</code> &nbsp;
<code>.webm</code>
</p>

<h3>Example Prediction</h3>

<pre><code>Prediction: Violence
Confidence: 81.00%</code></pre>
