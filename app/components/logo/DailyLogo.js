import React from 'react';

import {Row, Col} from 'react-bootstrap/lib/';

export default function DailyLogo() {
    return(
        <Row>
            <Col xs={12} sm={8}  md={8} xsOffset={2} mdOffset={3}>
                <div id='logo-header' className='logo'>
                    <spam className='daily'> Daily </spam><i className='fa fa-globe fa-lg' /><spam className='planet'> Planet </spam>
                </div>
            </Col>
        </Row>

    )
}