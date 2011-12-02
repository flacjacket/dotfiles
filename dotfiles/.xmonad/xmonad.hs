import XMonad
import qualified XMonad.StackSet as S
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.ManageHelpers
import XMonad.Layout.Grid
import XMonad.Layout.IM
import XMonad.Layout.Named
import XMonad.Layout.NoBorders
import XMonad.Layout.PerWorkspace
import XMonad.Layout.Reflect
import XMonad.Util.EZConfig(additionalKeys)
import XMonad.Util.Run(spawnPipe)

import Data.Ratio
import System.IO

-- Set mod key
myModMask = mod4Mask

-- Set default configuration
myBaseConfig = defaultConfig

-- Set default terminal
myTerminal = "urxvt"

-- Set up borders
myBorderWidth = 1
myNormalBorderColor = "#202030"
myFocusedBorderColor = "#A0A0D0"

-- Set workspaces
myWorkspaces = (miscs 5) ++ ["6-music", "7-fullscreen", "8-skype", "9-im"]
	where miscs = map (("" ++) . show) . (flip take) [1..]

-- Set Layouts
basicLayout = Tall nmaster delta ratio where
		nmaster	= 1
		delta	= 3/100
		ratio	= 1/2
tallLayout = named "tall" $ avoidStruts $ basicLayout
wideLayout = named "wide" $ avoidStruts $ Mirror basicLayout
singleLayout = named "single" $ avoidStruts $ noBorders Full
fullscreenLayout = named "fullscreen" $ noBorders Full
imLayout = avoidStruts $ withIM (1%6) (ClassName "Pidgin") Grid
skypeLayout = avoidStruts $ withIM (1%6) (Or (Title "sean.vig - Skype™ (Beta)") (Title "Skype™ 2.2 (Beta) for Linux")) Grid

myLayoutHook = fullscreen $ im $ skype $ normal where
	normal		= tallLayout ||| wideLayout ||| singleLayout
	fullscreen	= onWorkspace "7-fullscreen" fullscreenLayout
	skype		= onWorkspace "8-skype" skypeLayout
	im			= onWorkspace "9-im" imLayout

-- put the Pidgin and Skype windows in the im workspace
myManageHook = imManageHooks <+> fullscreenHooks <+> manageDocks <+> manageHook myBaseConfig
imManageHooks = composeAll [className =? "Pidgin" --> moveToIM
	, className =? "Skype" --> moveToSkype
	, className =? "MPlayer" --> doShift "fullscreen"
	, className =? "Canvas" --> doFloat
	, className =? "net-minecraft-LauncherFrame" --> doFloat
	, className =? "qemu-system-x86_64" --> doFloat
	, className =? "qemu" --> doFloat
	, className =? "net-yapbam-gui-Launcher" --> doFloat
	, className =? "Gnuplot" --> doFloat] where
		moveToIM = doF $ S.shift "9-im"
		moveToSkype = doF $ S.shift "8-skype"
fullscreenHooks = isFullscreen --> doFullFloat

-- Setup bar colors
myNormalBGColor  = "#2e3436"
myFocusedBGColor = "#414141"
myNormalFGColor  = "#E0FFFF"
myFocusedFGColor = "#1994d1"
myUrgentFGColor  = "#f57900"
myUrgentBGColor  = "#2e3436"
myVisibleBGColor = "#515151"

xmonadDir = "/home/sean/.xmonad"

-- Setup dzen bar
myWorkspaceBar = "dzen2 -ta l -h 13 -w 920 -x 0 -fn '-*-terminus-*-r-normal-*-*-120-*-*-*-*-iso8859-*' -bg '#2c2c32' -fg 'grey70' -p"

mydzenPP handle = defaultPP
	{ ppCurrent	= wrap("^fg(" ++ myFocusedFGColor ++ ")^bg(" ++ myFocusedBGColor ++ ")^p(2)") "^p(4)^fg()^bg()"
	, ppUrgent	= wrap ("^fg(" ++ myUrgentFGColor ++ ")^bg(" ++ myUrgentBGColor ++ ")^p(2)") "^p(4)^fg()^bg()"
	, ppVisible	= wrap ("^fg(" ++ myNormalFGColor ++ ")^bg(" ++ myNormalBGColor ++ ")^p(2)") "^p(4)^fg()^bg()"
	, ppHidden	= wrap ("^fg(" ++ myNormalFGColor ++ ")^bg(" ++ myVisibleBGColor ++ ")^p(2)") "^p(4)^fg()^bg()"
	, ppSep		= ""
	, ppOutput	= hPutStrLn handle
	, ppTitle	= dzenColor myNormalFGColor "" . wrap "< " " >"
	, ppLayout	= dzenColor myFocusedFGColor "" . wrap "^p(4)" "^p(4)"
	}

-- Main
main = do
	workspacebarpipe <- spawnPipe myWorkspaceBar
	xmonad $ myBaseConfig
		{ modMask			= myModMask
		, layoutHook		= myLayoutHook
		, manageHook		= myManageHook
		, workspaces		= myWorkspaces
		, terminal			= myTerminal
		, borderWidth		= myBorderWidth
		, normalBorderColor	= myNormalBorderColor
		, focusedBorderColor= myFocusedBorderColor
		, logHook			= dynamicLogWithPP $ mydzenPP workspacebarpipe
		}
