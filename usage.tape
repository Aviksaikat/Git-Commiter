Output "media/usecase.gif"
Set Shell zsh
Set FontSize 25
Set Width 1280
Set Height 720
Set FontFamily "ubuntumono Nerd Font mono"
Set Theme "Andromeda"
# You'll likely want to add a Margin + MarginFill if you use BorderRadius.
# Set Margin 20
# Set MarginFill "#8ABDEC"
# Set BorderRadius 10
Set Framerate 60
Type "gitcommiter -d ."
Enter
Type "git log -1 --stat | awk '/Date/ {flag=1} /2 files changed/ {flag=0} flag'"
Enter
Sleep 10s