
FROM python:3.9

ARG SC2_VERSION=4.10

USER root

# Update system
RUN apt-get update \
    && apt-get upgrade --assume-yes --quiet=2 \
    # Update and install packages for SC2 development environment
    # git, unzip and wget for download and extraction
    # rename to rename maps
    # tree for debugging
    && apt-get install --assume-yes --no-install-recommends --no-show-upgraded \
    git  \
    unzip \
    wget \
    rename \
    tree

WORKDIR /root/bot/

# copy everything to the container
COPY . .

# install dependencies of the app
RUN pip install -r requirements.txt

WORKDIR /root/Documents/

# Download and uncompress StarCraftII from https://github.com/Blizzard/s2client-proto#linux-packages and remove zip file
# If file is locally available, use this instead:
#ADD SC2.4.10.zip /root/
RUN wget --quiet --show-progress --progress=bar:force http://blzdistsc2-a.akamaihd.net/Linux/SC2.$SC2_VERSION.zip \
    && unzip -q -P iagreetotheeula SC2.$SC2_VERSION.zip \
    && rm SC2.$SC2_VERSION.zip \
    # Create a symlink for the maps directory
    && ln -s /root/Documents/StarCraftII/Maps /root/Documents/StarCraftII/maps \
    # Remove the Maps that come with the SC2 client
    && rm -rf /root/Documents/StarCraftII/maps/* \
    # Remove Battle.net folder
    && rm -rf /root/Documents/StarCraftII/Battle.net/* \
    # Remove Shaders folder
    && rm -rf /root/Documents/StarCraftII/Versions/Shaders*

# Change to maps folder
WORKDIR /root/Documents/StarCraftII/maps/

# Maps are available here https://github.com/Blizzard/s2client-proto#map-packs and here http://wiki.sc2ai.net/Ladder_Maps
# Download and uncompress StarCraftII Maps, remove zip file - using "maps" instead of "Maps" as target folder

# Get ladder maps
RUN wget --quiet --show-progress --progress=bar:force \
    https://archive.sc2ai.net/Maps/Season1Maps.zip \
    https://archive.sc2ai.net/Maps/Season2Maps.zip \
    https://archive.sc2ai.net/Maps/Season3Maps.zip \
    https://archive.sc2ai.net/Maps/Season4Maps.zip \
    https://archive.sc2ai.net/Maps/Season5Maps.zip \
    https://archive.sc2ai.net/Maps/Season6Maps.zip \
    https://archive.sc2ai.net/Maps/Season7Maps.zip \
    https://archive.sc2ai.net/Maps/Season8Maps.zip \
    https://archive.sc2ai.net/Maps/Season9Maps.zip \
    https://archive.sc2ai.net/Maps/Season10Maps.zip \
    && unzip -q -o '*.zip' \
    && rm *.zip \
    # Get official blizzard maps
    && wget --quiet --show-progress --progress=bar:force http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2019Season3.zip \
    && unzip -q -P iagreetotheeula -o 'Ladder2019Season3.zip' \
    && mv Ladder2019Season3/* . \
    && rm Ladder2019Season3.zip \
    && rm -r Ladder2019Season3 \
    # Get v5.0.6 maps
    && wget --quiet --show-progress --progress=bar:force https://github.com/shostyn/sc2patch/raw/master/Maps/506.zip \
    && unzip -q -o '506.zip' \
    && rm 506.zip \
    # Get flat and empty maps
    && wget --quiet --show-progress --progress=bar:force http://blzdistsc2-a.akamaihd.net/MapPacks/Melee.zip \
    && unzip -q -P iagreetotheeula -o 'Melee.zip' \
    && mv Melee/* . \
    && rm Melee.zip \
    && rm -r Melee \
    # Get Sc2 AI Arena 2022 Season 3
    && wget --quiet --show-progress --progress=bar:force https://sc2ai.net/wiki/184/plugin/attachments/download/14/ \
    && unzip -q -o '*.zip' \
    && rm *.zip \
    # Remove LE suffix from file names
    && rename -v 's/LE.SC2Map/.SC2Map/' *.SC2Map \
    # List all map files
    && tree

WORKDIR /root/

ENTRYPOINT [ "/bin/bash" ]