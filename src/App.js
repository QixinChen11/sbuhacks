import React, { useState, useEffect } from 'react';
import './App.css';
import { IconButton, Drawer, TextField, Button } from '@material-ui/core';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import Typography from '@material-ui/core/Typography';
import 'react-circular-progressbar/dist/styles.css';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import BubbleChart from '@weknow/react-bubble-chart-d3';
import axios from 'axios';


const App = () => {
	const [drawer, setDrawer] = useState(true);
	const [submit, setSubmit] = useState(false);
	const [dWidth, setWidth] = useState(380);
	const [artistName, setArtist] = useState('');
	const [songName, setSong] = useState('');
	const [lyrics, setLyrics] = useState('');
	const [data, setData] = useState([]);
	const [hit, setHit] = useState("");


	const handleSubmit = () => {
		fetch('http://localhost:5000/top').then((res) => {
			return res.json();
		}).then((data) => {
			setSubmit(true);
			setWidth(40);
			setDrawer(false);
			let freqs = [];
            data['lyrics'].forEach((element) => {
				freqs.push({
					label: element[0],
					value: element[1]
				});
			});
			setData(freqs);
			console.log(freqs);
		});

		fetch('http://localhost:5000/predict', {
			method: 'POST',
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({
				lyrics: lyrics
			})
		})
			.then(resp => resp.json())
			.then(data => {
				try {
					setHit(data.n);
				} catch (e) {
					console.error(e);
				}
			});
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
				{submit ? (
					<div className="body">
						<h1> {songName + ' ' + artistName}</h1>
								value={69}
						/>
					</div>
				) : (
					<div></div>
				)}
			</div>
		</div>
	);
};

export default App;
