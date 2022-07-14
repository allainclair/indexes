## Frontend

### React

0. Create folder webapp and `$ cd webapp`.

1. `$ npx create-react-app frontend`.

2. Remove unnecessary files from installation.

3. `$ cd webapp/frontend/`.

## Material

`$ npm install @material-ui/core`

`npm install fontsource-roboto`  Talvez nao precise

## Recharts

`$ npm install recharts`

## Nivo NOT USED. dependency issues

yarn add @nivo/core @nivo/line

### Chakra UI -- Not needed yet

4. `$ npm i @chakra-ui/react @emotion/react @emotion/styled framer-motion`

### Deploy github pages

https://create-react-app.dev/docs/deployment/

```
# package.json
"script": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -b BRANCH_OF_THE_SITE -d build",
}
```

