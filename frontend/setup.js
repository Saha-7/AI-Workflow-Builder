#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('Setting up GenAI Stack Frontend...');

// Create .env file if it doesn't exist
const envFile = '.env';
if (!fs.existsSync(envFile)) {
  console.log('Creating .env file...');
  const envContent = `REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
`;
  fs.writeFileSync(envFile, envContent);
  console.log('✅ .env file created');
} else {
  console.log('✅ .env file already exists');
}

// Create public directory if it doesn't exist
const publicDir = 'public';
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
  console.log('✅ Public directory created');
}

// Create src directory structure if it doesn't exist
const srcDirs = ['components', 'pages', 'hooks', 'services', 'types', 'utils'];
srcDirs.forEach(dir => {
  const dirPath = path.join('src', dir);
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`✅ ${dir} directory created`);
  }
});

console.log('\n🎉 Frontend setup completed!');
console.log('\nTo start the frontend:');
console.log('  npm start');
console.log('\nTo test the frontend:');
console.log('  Visit http://localhost:3000/test');
console.log('\nTo build for production:');
console.log('  npm run build');
