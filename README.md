# audio-identification-reproduction

```
git clone https://github.com/jasper-zheng/audio-identification-reproduction.git
cd audio-identification-reproduction
```

To build the fingerprint databese: make sure audio files in `database_recordings.zip` are extracted to `datasets/database_recordings`, then run:

```
from audio_fingerprint import fingerprintBuilder

fingerprintBuilder('datasets/database_recordings', 'datasets/fingerprint_database.p')

```

To identify a folder of queries: make sure query audio files are extracted to `datasets/query_recordings`, then run:

```
from audio_identification import audioIdentification

audioIdentification('datasets/query_recordings', 'datasets/fingerprint_database.p', 'output.txt')

```

