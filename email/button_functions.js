app.post('/resolve-ticket/:num', async (req, res) => {
    const { ticketId } = req.body;

    try {


    const num = req.params.num;
        const result = await Ticket.updateOne(
            { _id: ticketId },
            { $set: { status: 'resolved' } }
        );

        if (result.modifiedCount === 0) {
            return res.status(404).json({ message: 'Ticket not found or already resolved' });
        }

        res.status(200).json({ message: 'Ticket resolved successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Internal Server Error' });
    }
});


app.post('/raise-ticket', async (req, res) => {
    const { ticketDetails } = req.body;  
    try {
        const response = await externalTicketingAPI(ticketDetails); 
        if (response.status !== 200) {
            return res.status(400).json({ message: 'Failed to raise ticket' });
        }

        const ticketNumber = response.data.ticketNumber;
        res.status(200).json({ message: 'Ticket raised successfully', ticketNumber });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Internal Server Error' });
    }
});

async function externalTicketingAPI(details) {
    // Simulate calling an external API
    return {
        status: 200,
        data: { ticketNumber: 'TICKET12345' },
    };
}
