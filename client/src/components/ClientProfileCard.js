import React, { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient';
import { User, MapPin, Activity, ShoppingBag, Phone } from 'lucide-react';

const ClientProfileCard = ({ clientId }) => {
    const [client, setClient] = useState(null);
    const [attributes, setAttributes] = useState({});
    const [activations, setActivations] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (clientId) fetchClientData();
    }, [clientId]);

    const fetchClientData = async () => {
        setLoading(true);
        try {
            // 1. Fetch Core Identity
            const { data: clientData, error: clientError } = await supabase
                .from('clients')
                .select('*')
                .eq('id', clientId)
                .single();

            if (clientError) throw clientError;
            setClient(clientData);

            // 2. Fetch DNA Attributes (The EAV Data)
            const { data: attrData, error: attrError } = await supabase
                .from('client_dna_attributes')
                .select('*')
                .eq('client_id', clientId);

            if (attrError) throw attrError;

            // Group attributes by Root Category for display
            // Result: { "Lifestyle": [attr1, attr2], "Identité": [attr3] ... }
            const grouped = attrData.reduce((acc, curr) => {
                const root = curr.root_category;
                if (!acc[root]) acc[root] = [];
                acc[root].push(curr);
                return acc;
            }, {});
            setAttributes(grouped);

            // 3. Fetch Activations (Next Actions)
            const { data: actData, error: actError } = await supabase
                .from('activations')
                .select('*')
                .eq('client_id', clientId)
                .order('deadline', { ascending: true });

            if (actError) throw actError;
            setActivations(actData);

        } catch (error) {
            console.error('Error fetching client DNA:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="p-6 text-center text-gray-500">Loading Profile...</div>;
    if (!client) return <div className="p-6 text-center text-red-500">Client not found</div>;

    return (
        <div className="bg-white rounded-[24px] shadow-sm border border-gray-100 p-6 max-w-4xl mx-auto font-sans">

            {/* HEADER: Identity */}
            <div className="flex justify-between items-start mb-8 border-b border-gray-100 pb-6">
                <div className="flex gap-4">
                    <div className="h-16 w-16 rounded-full bg-[#1A1A1A] text-white flex items-center justify-center text-2xl font-bold">
                        {client.full_name.charAt(0)}
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-[#111]">{client.full_name}</h2>
                        <div className="flex items-center gap-2 mt-1">
                            <span className="px-3 py-1 bg-[#1A1A1A] text-white text-xs rounded-full font-medium">{client.status}</span>
                            <span className="text-sm text-gray-500">{client.email}</span>
                        </div>
                    </div>
                </div>
                <div className="text-right">
                    <p className="text-sm text-gray-400">Client since</p>
                    <p className="font-medium text-[#111]">{new Date(client.created_at).toLocaleDateString()}</p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

                {/* LEFT COL: DNA Attributes (Grouped) */}
                <div className="md:col-span-2 space-y-6">
                    <h3 className="text-lg font-bold flex items-center gap-2"><User size={20} /> Client DNA</h3>

                    {Object.keys(attributes).map((root) => (
                        <div key={root} className="bg-gray-50 rounded-xl p-4">
                            <h4 className="text-sm font-bold text-[#C87961] uppercase mb-3 tracking-wide">{root}</h4>
                            <div className="grid grid-cols-2 gap-y-3 gap-x-4">
                                {attributes[root].map((attr) => (
                                    <div key={attr.id} className="flex flex-col">
                                        <span className="text-[11px] text-gray-400 font-medium">{attr.sub_category}</span>
                                        <span className="text-[13px] text-[#111] font-semibold">{attr.value}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>

                {/* RIGHT COL: Activations & Stats */}
                <div className="space-y-6">

                    {/* Next Action */}
                    <div className="bg-[#FFF8F6] border border-[#F5E6E3] rounded-xl p-5">
                        <h3 className="text-md font-bold text-[#9A422E] flex items-center gap-2 mb-3">
                            <Activity size={18} /> Next Activation
                        </h3>
                        {activations.length > 0 ? (
                            <div>
                                <p className="text-lg font-bold text-[#111]">{activations[0].action_type}</p>
                                <div className="flex justify-between items-center mt-2">
                                    <span className="text-sm text-gray-500">via {activations[0].channel}</span>
                                    <span className="text-xs font-medium bg-white px-2 py-1 rounded border border-[#F5E6E3] text-[#9A422E]">
                                        {new Date(activations[0].deadline).toLocaleDateString()}
                                    </span>
                                </div>
                            </div>
                        ) : (
                            <p className="text-sm text-gray-500 italic">No pending actions</p>
                        )}
                    </div>

                </div>
            </div>
        </div>
    );
};

export default ClientProfileCard;
