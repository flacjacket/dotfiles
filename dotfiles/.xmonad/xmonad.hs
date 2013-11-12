import XMonad
import Control.Monad
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.EwmhDesktops
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.ManageHelpers
import XMonad.Layout.PerWorkspace
import XMonad.Layout.Named
import XMonad.Layout.NoBorders
import XMonad.StackSet(current,screen,visible,screenDetail)
import XMonad.Util.EZConfig(additionalKeys)
import XMonad.Util.Loggers
import XMonad.Util.Run(spawnPipe)
import System.IO

-- Set mod key
myModMask = mod4Mask

-- Set default configuration
myBaseConfig = defaultConfig

--Set up display
myBorderWidth = 2
myNormalBorderColor = "#202030"
myFocusedBorderColor = "#A0A0D0"

myFont = "-*-terminus-*-r-normal-*-*-90-*-*-*-*-iso8859-*"

-- Set default terminal
myTerminal = "urxvt"

-- Set workspaces
myWorkspaces = (miscs 8) ++ ["fullscreen"]
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

myLayoutHook = fullscreen $ normal where
	normal     = tallLayout ||| wideLayout ||| singleLayout
	fullscreen = onWorkspace "fullscreen" fullscreenLayout

myManageHook = floatManageHooks <+> fullscreenManageHooks <+> manageDocks <+> manageHook myBaseConfig
floatManageHooks = composeAll[
        className =? "mplayer"        --> doFloat
      , className =? "sun-awt-X11-XFramePeer" --> doFloat
      , className =? "processing-app-Base" --> doFloat
	  , className =? "Canvas"         --> doFloat
      , title =? "PyEELS"             --> doFloat
      , className =? "stalonetray"    --> doIgnore
    ]
fullscreenManageHooks = isFullscreen --> doFullFloat

-- Setup dzen bar
myWorkspaceBar = "dzen2 -xs 1 -ta l -h 13 -w 1420 -x 0 -fn '" ++ myFont ++ "' -p"

myFocusedFGColor	= "white"
myTitleFGColor		= "green"

toggleStrutsKey XConfig{modMask = modm} = (modm, xK_b)

myDzenPP conf =
	statusBar
		myWorkspaceBar
		myDzenPP
		toggleStrutsKey
		conf
	where
		myDzenPP = dzenPP {
			  ppCurrent	= dzenColor myFocusedFGColor "" . wrap "<" ">"
			, ppVisible	= wrap "<" ">"
			, ppUrgent	= dzenColor "red" "" . pad
			, ppHidden	= pad
			, ppWsSep	= ""
			, ppLayout	= dzenColor myFocusedFGColor "" . wrap "^p(4)" "^p(4)"
			, ppTitle   = dzenColor myTitleFGColor "" . wrap "< " " >"
			}

-- Run everything
main = do
	xmonad =<< (myDzenPP =<< return mainConfig)

mainConfig = defaultConfig {
		  focusedBorderColor	= myFocusedBorderColor
		, handleEventHook		= fullscreenEventHook
		, layoutHook			= myLayoutHook
		, manageHook			= myManageHook
		, modMask				= myModMask
		, normalBorderColor		= myNormalBorderColor
		, terminal				= myTerminal
		, workspaces			= myWorkspaces
		} `additionalKeys`
		[ ((myModMask .|. shiftMask, xK_l), spawn "xscreensaver-command -lock")
		, ((myModMask, xK_i), spawn "ipython qtconsole --profile=sympy")
		, ((controlMask, xK_Print), spawn "sleep 0.2; scrot -s")
		, ((0, xK_Print), spawn "scrot")
		]
-- TODO: UrgencyHook
