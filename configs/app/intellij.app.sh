#!/bin/bash
NAME="intellij-idea-community-edition"
SHORT="idea"
yay -S $NAME --noconfirm

# install to jetbrains toolbox (if toolbox is installed)
TOOLBOX_PATH="/home/$(whoami)/.local/share/JetBrains/Toolbox"
if [[ -d "$TOOLBOX_PATH" ]]; then
    sudo mv /usr/share/$SHORT $TOOLBOX_PATH/apps/$NAME
    sudo chmod 777 -R $TOOLBOX_PATH/apps/$NAME
    ln -s $TOOLBOX_PATH/apps/$NAME/bin/$SHORT $TOOLBOX_PATH/scripts/$SHORT
fi

cp /usr/share/applications/idea.desktop ~/Desktop/idea.desktop