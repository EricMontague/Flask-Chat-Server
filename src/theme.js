// Based on Coinbase's color pallette as of February 11, 2021
// Site background color: #f7f9fc
// Top navbar color: #fafbfc
// Page title in navbar text color: #000000
// Primary gray text color for contrast: #738498
// Side navigation bar color: #ffffff
// Side navigation bar icon bg color: #f1f3f5
// Side navigation bar icon color (unselected): #050f19
// Side navigation bar icon color (selected): #1453f0
// Side navigation bar toast background color: #191919
// Side navigation bar toast text color: #fbfbfb
// Side navigation bar border color: #f1f3f5
// Cards background color: #ffffff
// Card title text color: #050f19

// Card border / box shadow
//     border: 1px solid rgb(236, 239, 241);
// box-shadow: rgb(17 51 83 / 2%) 0px 4px 12px 0px;
// width: auto;
// border-radius: 5px;

// List inside card border color: #edeff1
// Logo color: #1453f0
// Sign out text color (danger color?): #de5f67
// Success color: #0db068
// Overlay color when menus are open: #607185

// input field border color: #edeff1
// input field placeholder text color: #718295

// primary color: # 1453f0

const theme = {
    bg: {
        default: '#ffffff',
        primary: '#1453f0',
        light: '#fafbfc',
        warn: '#de5f67'
    },
    font: {
        default: `-apple-system, BlinkMacSystemFont, 'Segoe UI',
        Helvetica, Arial, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';`
    },
    text: {
        default: '#050f19',
        primary: '#1453f0',
        placeholder: '#718295',
        white: '#ffffff',
        warn: '#de5f67'
    },
    input: {
        border: '#e0e3e5',
        borderHover: '#ced4da',
        placeholder: '#718295',
    }
};

export default theme;