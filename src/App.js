import React, { useState, useEffect } from 'react';
import './App.css';
import { IconButton, Drawer, TextField, Button } from '@material-ui/core';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import Typography from '@material-ui/core/Typography';
import 'react-circular-progressbar/dist/styles.css';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';

const App = () => {
	const [drawer, setDrawer] = useState(true);
	const [submit, setSubmit] = useState(false);
	const [dWidth, setWidth] = useState(380);
	const [artistName, setArtist] = useState('');
	const [songName, setSong] = useState('');
	const [lyrics, setLyrics] = useState('');

	const handleSubmit = () => {
		console.log(artistName, songName, lyrics);
		setSubmit(true);
		setWidth(40);
		setDrawer(false);
	};
	const handleDrawer = () => {
		setWidth(380);
		setDrawer(!drawer);
		setSubmit(false);
	};

	return (
		<div style={{ backgroundColor: 'antiquewhite' }}>
			<div className="container">
				<IconButton
					style={{ height: '100vh', borderRadius: '0px' }}
					color="inherit"
					edge="end"
					onClick={handleDrawer}
					id="rightArrow"
				>
					<ChevronRightIcon />
				</IconButton>
				<div className="drawer">
					<Drawer variant="persistent" anchor="left" open={drawer} PaperProps={{ elevation: 20 }}>
						<div className="drawerContent">
							<h1 style={{ textAlign: 'center', minWidth: '400px' }}>Hit prediction</h1>
							<TextField
								id="standard-required"
								margin="normal"
								label="Enter Artist Name"
								multiline
								variant="outlined"
								required
								onChange={e => {
									setArtist(e.target.value);
								}}
							/>
							<TextField
								id="standard-required"
								margin="normal"
								label="Enter Song Name"
								multiline
								variant="outlined"
								required
								onChange={e => {
									setSong(e.target.value);
								}}
							/>
							<TextField
								id="standard-required"
								margin="normal"
								label="Enter Lyrics"
								multiline
								rowsMax="20"
								variant="outlined"
								required
								onChange={e => {
									setLyrics(e.target.value);
								}}
							/>
							<br />
							<Button
								id="button"
								type="submit"
								variant="contained"
								color="primary"
								onClick={handleSubmit}
							>
								Submit
							</Button>
						</div>
					</Drawer>
				</div>
				<div className="body" style={{ marginLeft: `${dWidth}px` }}>
					{submit ? <h1> {songName + ' ' + artistName}</h1> : <div></div>}

					<Typography paragraph>
						Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
						labore et dolore magna aliqua. Rhoncus dolor purus non enim praesent elementum facilisis leo
						vel. Risus at ultrices mi tempus imperdiet. Semper risus in hendrerit gravida rutrum quisque non
						tellus. Convallis convallis tellus id interdum velit laoreet id donec ultrices. Odio morbi quis
						commodo odio aenean sed adipiscing. Amet nisl suscipit adipiscing bibendum est ultricies integer
						quis. Cursus euismod quis viverra nibh cras. Metus vulputate eu scelerisque felis imperdiet
						proin fermentum leo. Mauris commodo quis imperdiet massa tincidunt. Cras tincidunt lobortis
						feugiat vivamus at augue. At augue eget arcu dictum varius duis at consectetur lorem. Velit sed
						ullamcorper morbi tincidunt. Lorem donec massa sapien faucibus et molestie ac.
					</Typography>
					<div className="circularBar">
						<CircularProgressbar
							value={69}
							text={`69%`}
							background
							backgroundPadding={6}
							styles={buildStyles({
								backgroundColor: '#3e98c7',
								textColor: '#fff',
								pathColor: '#fff',
								trailColor: 'transparent',
							})}
						/>
					</div>
				</div>
			</div>
		</div>
	);
};

export default App;
