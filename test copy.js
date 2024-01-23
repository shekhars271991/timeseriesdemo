#!js name=StreamTrigger1 api_version=1.0
redis.registerStreamTrigger(
    "consumer", // consumer name
    "stream", // streams prefix
    function(c, data) {
        const records = data.record;
        const unit_data_args = [];
        i = 0;
        records.forEach(record => {
             c.call('set','hello:count:'+i, record[0]);
             i++;
            // Check if the first element of the subarray is "Business Unit"
            if (record[0] === "business_unit") {
                // If it is, do something with the record or call your function
                stream_name = record[1]
                
            }
            else{
                unit_data_args.push(record[0], record[1]);
            }
        });

        // var curr_time = c.call("time")[0];

        c.call('set','hello:skr', stream_name);
        // c.call('set','hello:skr1', unit_data);
        c.call('xadd', stream_name, "*", ...unit_data_args);
        
    }
);