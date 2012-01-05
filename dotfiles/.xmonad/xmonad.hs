import XMonad
import qualified XMonad.StackSet as S
import Control.Monad
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.ManageHelpers
import XMonad.Layout.LayoutModifier
import XMonad.Layout.Grid
import XMonad.Layout.PerWorkspace
import XMonad.Layout.Named
import XMonad.Layout.IM
import XMonad.Layout.NoBorders
import XMonad.Layout.Reflect
import XMonad.Util.Run(spawnPipe)
import XMonad.Util.EZConfig(additionalKeys)
import XMonad.Util.WindowProperties
import Data.Ratio
import System.IO

-- Set mod key
myModMask = mod4Mask

-- Set default configuration
myBaseConfig = defaultConfig

--Set up display
myBorderWidth = 2
myNormalBorderColor = "#202030"
myFocusedBorderColor = "#A0A0D0"

-- Set default terminal
myTerminal = "urxvt"

-- Set workspaces
myWorkspaces = (miscs 3) ++ ["web", "email", "gimp", "music", "fullscreen", "im"]
    where miscs = map (("" ++) . show) . (flip take) [1..]
-- isFullscreen = (== "fullscreen")

-- Set layouts
basicLayout = Tall nmaster delta ratio where
		nmaster = 1
		delta   = 3/100
		ratio   = 1/2
tallLayout = named "tall" $ avoidStruts $ basicLayout
wideLayout = named "wide" $ avoidStruts $ Mirror basicLayout
singleLayout = named "single" $ avoidStruts $ noBorders Full
fullscreenLayout = named "fullscreen" $ noBorders Full
imLayout = avoidStruts $ reflectHoriz $ withIM (1%6) (ClassName "Pidgin") Grid
--	chatLayout      = Grid
--	ratio           = 1%6
--	rosters			= [pidginRoster]
--	pidginRoster    = And (ClassName "Pidgin") (Role "buddy_list")
--	skypeRoster     = (ClassName "Skype") `And` (Not (Title "Options")) `And` (Not (Role "Chats")) `And` (Not (Role "CallWindowForm")

myLayoutHook = fullscreen $ im $ normal where
	normal     = tallLayout ||| wideLayout ||| singleLayout
	fullscreen = onWorkspace "fullscreen" fullscreenLayout
	im         = onWorkspace "im" imLayout

-- put the Pidgin and Skype windows in the im workspace
myManageHook = imManageHooks <+> facebookManageHooks <+> manageDocks <+> manageHook myBaseConfig
imManageHooks = composeAll [isIM --> moveToIM
	, className =? "mplayer" --> doFloat
	, className =? "Canvas" --> doFloat
	, className =? "Chromium" --> doShift "web"] where
		isIM     = foldr1 (<||>) [isPidgin, isSkype]
		isPidgin = className =? "Pidgin"
		isSkype  = className =? "Skype"
		moveToIM = doF $ S.shift "im"
facebookManageHooks = isFullscreen --> doFullFloat

-- Setup dzen bars
myWorkspaceBar = "dzen2 -ta l -h 13 -w 640 -x 0 -fn '-*-terminus-*-r-normal-*-*-90-*-*-*-*-iso8859-*' -bg '#2c2c32' -fg 'grey70' -p"
myStatusBar = "/home/sean/.dzen/dzenscript | dzen2 -ta r -h 13 -w 640 -x 640 -fn '-*-terminus-*-r-normal-*-*-90-*-*-*-*-iso8859-*' -bg '#2c2c32' -fg 'grey70' -p"

myNormalFGColor = "green"

mydzenPP handle = defaultPP
	{ ppOutput 	= hPutStrLn handle
	, ppTitle       = dzenColor myNormalFGColor "" . wrap "< " " >"
	}

--	{ ppCurrent	= wrap("^fg(" ++ myFocusedFGColor ++ ")^bg(" ++ myFocusedBGColor ++ ")^p(2)") "^p(4)^fg()^bg()"
--	, ppUrgent	= wrap ("^fg(" ++ myUrgentFGColor ++ ")^bg(" ++ myUrgentBGColor ++ ")^p(2)") "^p(4)^fg()^bg()"
--	, ppVisible	= wrap ("^fg(" ++ myNormalFGColor ++ ")^bg(" ++ myNormalBGColor ++ ")^p(2)") "^p(4)^fg()^bg()"
--	, ppHidden	= wrap ("^fg(" ++ myNormalFGColor ++ ")^bg(" ++ myVisibleBGColor ++ ")^p(2)") "^p(4)^fg()^bg()"
--	, ppSep		= ""
--	, ppOutput	= hPutStrLn handle
--	, ppTitle	= dzenColor myNormalFGColor "" . wrap "< " " >"
--	, ppLayout	= dzenColor myFocusedFGColor "" . wrap "^p(4)" "^p(4)"
--	}

-- Run everything
main = do
	workspacebarpipe <- spawnPipe myWorkspaceBar
--	statusbarpipe <- spawnPipe myStatusBar
	xmonad $ defaultConfig
		{ modMask		= myModMask
		, workspaces		= myWorkspaces
		, manageHook		= myManageHook
		, layoutHook		= myLayoutHook
		, terminal		= myTerminal
		, normalBorderColor	= myNormalBorderColor
		, focusedBorderColor	= myFocusedBorderColor
		, logHook		= dynamicLogWithPP $ mydzenPP workspacebarpipe
		} `additionalKeys`
		[ ((myModMask .|. shiftMask, xK_l), spawn "xscreensaver-command -lock")
		, ((controlMask, xK_Print), spawn "sleep 0.2; scrot -s")
		, ((0, xK_Print), spawn "scrot")
		]
