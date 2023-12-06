import * as React from 'react';
import { useState } from 'react';
import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import { Grid, Paper } from '@mui/material';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
// import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const VisuallyHiddenInput = styled('input')({
    clip: 'rect(0 0 0 0)',
    clipPath: 'inset(50%)',
    height: 1,
    overflow: 'hidden',
    position: 'absolute',
    bottom: 0,
    left: 0,
    whiteSpace: 'nowrap',
    width: 1,
});

export default function InputFileUpload() {

    const [resultData, setResultData] = useState({
        "prediction_protein": 0,
        "prediction_carbohydrates": 0,
        "prediction_fats": 0,
    })


    const Submit = (e) => {
        const formData = new FormData();
        formData.append("file", e.target.files[0]);
        console.log(formData);
        const response = fetch(`http://localhost:8000/classification_cnn`, {
            method: 'POST',
            body: formData
        }).then(r => r.json()).then(data => setResultData(data));


    }
    return (
        <Grid container justifyContent='center' spacing={4}>
            <Grid container item xs={12} justifyContent='center'>
                <Button component="label" variant="contained" >
                    Upload file
                    <VisuallyHiddenInput onChange={Submit} type="file" />
                </Button>
            </Grid>
            <Grid item xs={9}>
                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell><b>Nutrients</b></TableCell>
                                <TableCell align="right"><b>Value&nbsp;(/100g)</b></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            
                            <TableRow
                                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                <TableCell component="th" scope="row">
                                    Protein
                                </TableCell>
                                <TableCell align="right">{resultData.prediction_protein}</TableCell>
                            </TableRow>
                            <TableRow
                                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                <TableCell component="th" scope="row">
                                    Carbohydrates
                                </TableCell>
                                <TableCell align="right">{resultData.prediction_carbohydrates}</TableCell>
                            </TableRow>
                            <TableRow
                                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                <TableCell component="th" scope="row">
                                    Fats
                                </TableCell>
                                <TableCell align="right">{resultData.prediction_fats}</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </TableContainer>
            </Grid>

        </Grid>

    );
}