# How to install

>! THIS IS NOT COMPLETE YET SORRY !

This page explains how to set up the dev environment for orchard2.

These will likely work as-is for MacOS and Linux users. Windows users are recommended to
use WSL (Windows Subsystem for Linux) to run the commands below.

## Clone the repo

Clone the repository:

```bash
$ git clone https://github.com/auburnsummer/orchard2.git
```

In the root directory, copy the example Procfile into `Procfile`:

```bash
$ cd orchard2
$ cp Procfile.example Procfile
```

The Procfile is used to run the application and its dependencies. Each line in the Procfile represents a process that will be run by the application.

In the `server/cafe-backend` directory, copy the example environment file into `.env`:

```bash
$ cd server/cafe-backend
$ cp .env.example .env
```

## Setup a HTTP tunnel

You will need a HTTP tunnel to expose your local server to the internet. This is necessary for Discord to communicate with the bot.

We will show two options in this guide: [ngrok](https://ngrok.com/) and [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/). I use Cloudflare Tunnels but be aware that you'll need a domain name for it to work. The cheapest domain names are the six-digit `.xyz` domains, which you can get for about $1.50 per year from various registrars.

Ngrok does not require a domain name but you won't have a custom domain for your tunnel.

### Using ngrok

1. Follow steps 1-3 here: https://ngrok.com/docs/getting-started/   
2. Step 5 shows the command to run ngrok. Replace `8080` with `8000` to match the port used by the backend server.
3. Copy the command into the Procfile in the `server/cafe-backend` directory, prefixing it with `ngrok:`, e.g.

   ```bash
   ngrok: ngrok http 8000 --url https://wubba-dubba-dubba-is-that-true.ngrok.io
   ```

### Using Cloudflare Tunnel

1. Make a tunnel here: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-remote-tunnel/
    - select Cloudflared as the type
    - In the Public Hostnames section, click "Add a public hostname"
    - Enter hostname as desired
    - Enter service as `http://localhost:8000`
2. Install Cloudflared by following the instructions here: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
3. In the page of the tunnel, there will be a command under the text "OR run the tunnel manually in your current terminal session only:"
   - Copy this command and paste it into the Procfile in the `server/cafe-backend` directory, prefixing it with `cloudflared:`, e.g.

   ```bash
   cloudflared: cloudflared tunnel run --token whoa-you-go-big-guy
   ```

## Setup a discord application

 1. Navigate to https://discord.com/developers/applications
 2. Click "New Application" and fill out the form. You should end up at the application settings page with "General Information" selected on the left menu panel.
 3. Copy the Application ID and paste it into the `.env` file as `DISCORD_CLIENT_ID`
 4. Copy the Public Key and paste it into the `.env` file as `DISCORD_PUBLIC_KEY`
 5. On the left menu panel, click on "OAuth"
 6. Under "Client secret", click "Reset Secret" and copy the new secret into the `.env` file as `DISCORD_CLIENT_SECRET` 
 7. In the section labelled "Redirects", add the following URL: `https://<your-tunnel-domain>/oauth/discord/callback/`
    - Note the trailing slash at the end! It's important
    - Replace `<your-tunnel-domain>` with the domain you set up in the previous step (e.g., `wubba-dubba-dubba-is-that-true.ngrok.io` or your custom domain).
 8. On the left menu panel, click on "Bot"
 9. Under "Token", click "Reset Token" then copy the new token into the `.env` file as `DISCORD_BOT_TOKEN`
 10. Don't close the window, we'll need it later.

## Install third party services

### Redis

Redis is used as a dependency for the Huey task queue, which is used to run background tasks in the application. The relevant variables in the `.env` are: `REDIS_HOST`, `REDIS_PORT`, and `REDIS_PASSWORD`. Typically, if you are running Redis locally, you can set `REDIS_HOST` to `localhost`, `REDIS_PORT` to `6379`, and leave `REDIS_PASSWORD` empty. If you are using a hosted Redis service, you will need to set these variables accordingly. These instructions assume you are running Redis locally.

1. Install Redis by following the instructions here: https://redis.io/docs/getting-started/installation/
2. The Procfile assumes that Redis is not running as a service. Instead, it's started when the app is running.
   - If you are running Redis as a service, you can remove the `redis-server` line from the Procfile since it will already be running.

### Typesense

Typesense is used for full-text search in the application. The relevant variables in the `.env` are: `TYPESENSE_API_HOST`, `TYPESENSE_API_PORT`, and `TYPESENSE_API_KEY`. If you are running Typesense locally, you can set `TYPESENSE_API_HOST` to `localhost`, `TYPESENSE_API_PORT` to `8108`, and set a random string as `TYPESENSE_API_KEY`. If you are using a hosted Typesense service, you will need to set these variables accordingly.

1. Install Typesense by following the instructions here: https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting
   - I recommend just downloading the binary into the root directory of the project and running it from there.
2. Create an empty folder called `data.typesense` in the root directory of the project. This is where Typesense will store its data: 

```bash
$ mkdir data.typesense
```

3. The Procfile assumes that Typesense is a binary file called `typesense-server` in the root directory of the project. If you have installed it elsewhere, you will need to change the command in the Procfile accordingly.
4. Alter the Procfile command to replace the `--api-key` value with whatever you set `TYPESENSE_API_KEY` to in the `.env` file, e.g. it might look like this:

```bash
$ typesense: ./typesense-server --api-key=xyz --data-dir=./data.typesense
```

### S3

S3 is used for file storage in the application. The relevant variables in the `.env` are: `S3_API_URL`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`, `S3_REGION`, and `S3_PUBLIC_CDN_URL`. For local development, you can use MinIO, which is an S3-compatible object storage server. If you are using a hosted S3 service, you will need to set these variables accordingly.

Otherwise the default values in the `.env` file should work ok for local development.

1. Install MinIO by following the instructions here: https://min.io/docs/minio/linux/index.html
2. Create a bucket called `orchard-dev` in MinIO. You can do this with the `mc` command line tool:

```bash
$ mc mb myminio/orchard-dev
```

3. Make the bucket public so that the files can be accessed without authentication. You can do this with the `mc` command line tool:

```bash
$ mc anonymous set public myminio/orchard-dev
```

## Install dependencies

 1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
 2. In the `server` directory, run the following command to install the Python dependencies:

```bash
$ uv sync
```

## Download test files

```bash
$ cd server/vitals/tests/fixtures
$ ./download_fixtures.sh
```

## Unit tests

To run the unit tests, you can use the following command:

```bash
$ uv run pytest
```

## Setup database

In the `server/cafe-backend` directory, set up the database tables:

```bash
$ uv run python manage.py migrate
```

Then create the test data:

```bash
$ uv run python manage.py seedtestdata
``` 

## Run the application

 1. Install a procfile runner. I use [Overmind](https://github.com/DarthSim/overmind) but you can use any procfile runner you like.
 2. In the root directory of the project, run the following command to start the application:

```bash
$ overmind start
```

(or whatever command your procfile runner uses to start the application)

 3. Open your web browser and navigate to the URL of your HTTP tunnel (e.g., `https://wubba-dubba-dubba-is-that-true.ngrok.io` or your custom domain). Confirm that the application is running and you can see the homepage. Confirm login works by clicking the "Login with Discord" button and logging in with your Discord account.

## Run the bot

 1. Keep the application running in the background.
 2. Open the Discord Application settings page you opened earlier.
 3. On the left menu panel, click on "General Information"
 4. Under the section "Interactions Endpoint URL", set the URL to `https://<your-tunnel-domain>/discord_interactions/`
    - Note the trailing slash at the end! It's important
    - Replace `<your-tunnel-domain>` with the domain you set up in the previous step (e.g., `wubba-dubba-dubba-is-that-true.ngrok.io` or your custom domain).
 5. Click "Save Changes". It should say "Interactions Endpoint URL updated successfully".
 6. TODO and then they should add the bot to a test server
 7. TODO and then they need to run the updatediscordslashcommands command from manage.py

