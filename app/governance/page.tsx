import { Callout, PageIntro, SectionHeading } from '@/components/ui';

export const metadata = { title: 'Research records' };
const responsibilities = [
  ['A7 registry', 'Project identities, relationships and authority routing', 'https://github.com/FabinGurung/JP_A7_System_Registry_and_Knowledge_Graph'],
  ['R&D hub', 'Research directory and reviewed public explanations', 'https://github.com/FabinGurung/JP_Research-and-Development'],
  ['A9 foundation', 'Governance schemas, operational checks and resume tools', 'https://github.com/FabinGurung/JP_Research-and-Development/tree/main/governance'],
  ['Google Drive', 'Original scientific sources, working documents and releases', null],
] as const;

export default function GovernancePage() {
  return <>
    <PageIntro eyebrow="Research records" title="Clear responsibilities for each record"
      summary="Research pages explain the work. Project registries identify it. Governance records track changes. Scientific evidence remains with its original authority." />
    <section className="section">
      <SectionHeading kicker="Responsibility" title="Where each record belongs" />
      <div className="table-scroll"><table className="governance-table"><caption>Research record responsibilities</caption>
        <thead><tr><th scope="col">Layer</th><th scope="col">Responsibility</th><th scope="col">Access</th></tr></thead>
        <tbody>{responsibilities.map(([name, role, url]) => <tr key={name}><th scope="row">{name}</th><td>{role}</td>
          <td>{url ? <a href={url}>Open repository</a> : 'Access through the owning research project'}</td></tr>)}</tbody>
      </table></div>
      <Callout title="One research hub, clear record boundaries" tone="blue"><p>The A9 foundation stays in the existing R&D repository. A separate private governance repository is an optional future choice for detailed or restricted records. Scientific evidence stays in Drive, and no scientific history has been migrated.</p></Callout>
      <p className="source-note"><span>Architecture source</span>The supplied research governance plan and the live A7 authority rules. Public project pages contain directory metadata and approved research modules.</p>
    </section>
  </>;
}
