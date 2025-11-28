@echo off
echo Generating animations...
echo.

echo [1/5] Generating Repeater...
python -m manim -pqh .\src\animations\qlearning\repeater_playback.py RepeaterPlayback
echo.

echo [2/5] Generating Counter...
python -m manim -pqh .\src\animations\qlearning\counter_playback.py CounterPlayback
echo.

echo [3/5] Generating Random...
python -m manim -pqh .\src\animations\qlearning\random_playback.py RandomPlayback
echo.

echo [4/5] Generating Slightbias...
python -m manim -pqh .\src\animations\qlearning\slightbias_playback.py SlightbiasPlayback
echo.

echo [5/5] Generating Fizzbuzz...
python -m manim -pqh .\src\animations\qlearning\fizzbuzz_playback.py FizzbuzzPlayback
echo.

echo All animations generated!
pause