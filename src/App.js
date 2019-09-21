import React, { useState, useEffect } from 'react';
import './App.css';
import { IconButton, Drawer, TextField, Button } from '@material-ui/core';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';

const App = () => {
	const [drawer, setDrawer] = useState(true);
	const handleDrawer = e => {
		setDrawer(!drawer);
	};
	return (
		<div style={{ backgroundColor: 'antiquewhite' }}>
			<div className="container">
				<IconButton
					style={{ height: '100vh', borderRadius: '0px' }}
					color="inherit"
					edge="end"
					onClick={handleDrawer}
				>
					<ChevronRightIcon />
				</IconButton>

				<Drawer variant="persistent" anchor="left" open={drawer} style={{borderRight:'groove'}}>
					<h1 style={{textAlign:'center'}}>
						Hit prediction
					</h1>
					<TextField
						id="standard-required"
						label="Required"
						margin="normal"
						helperText="Enter Artist Name"
					/>
					<TextField
						required
						id="standard-required"
						label="Required"
						margin="normal"
						helperText="Enter Lyrics"
						multiline
					/>
					<br />
					<Button type="submit"  variant="contained" color="primary" onClick={handleDrawer} style={{minWidth:'400px'}}>
						Submit
					</Button>
				</Drawer>
			</div>
		</div>
	);
};

export default App;
