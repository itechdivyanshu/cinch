const electron = require('electron');
const app = electron.app;

const path = require('path');
const url = require('url');
const nativeImage = electron.nativeImage;

let demoIcon =nativeImage.createFromPath(path.join(__dirname, 'icon.png'))

const BrowserWindow = electron.BrowserWindow;

var mainWindow;
app.on('ready',function(){
	mainWindow = new BrowserWindow({width: 1600, height: 1000,backgroundColor: '#2e2c29',icon:demoIcon,frame: false});
	mainWindow.setMenuBarVisibility(false);
	mainWindow.maximize();
	mainWindow.loadURL('http://127.0.0.1:8000');

});