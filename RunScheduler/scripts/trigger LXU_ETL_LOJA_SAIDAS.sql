
CREATE Trigger [dbo].[LXU_ETL_LOJA_SAIDAS]
 on [dbo].[LOJA_SAIDAS]
For Update Not For Replication
as
Begin

	SET CONTEXT_INFO 0x
	
  IF (SELECT CASE WHEN APP_NAME() LIKE '%LinxETL%' OR APP_NAME() LIKE '%datasync%' THEN 1 ELSE 0 END) = 0 OR (Isnull(CONTEXT_INFO(), 0x) != 0x53454D5F46494C415F45544C)
  Begin

   INSERT INTO  LJ_ETL_REPOSITORIO(TABELA,FILTRO,ID_ETL_TIPO,INDICA_EXCLUSAO)
   SELECT Distinct 'LOJA_SAIDAS', 'FILIAL='+Convert(Varchar(500),  inserted.FILIAL) +'{#}ROMANEIO_PRODUTO='+Convert(Varchar(500),  inserted.ROMANEIO_PRODUTO), LJ_LX_ETL_TIPO.Id_Etl_Tipo, 0 
   FROM Inserted
   Inner Join LJ_LX_ETL_TIPO  On LJ_LX_ETL_TIPO.Desc_Etl_Tipo = 'LOJA_SAIDAS'
   Where LJ_LX_ETL_TIPO.Inativo = 0 and LJ_LX_ETL_TIPO.Origem = 1 and Inserted.SAIDA_ENCERRADA = 1 AND Inserted.NUMERO_NF_TRANSFERENCIA not in ('','NULL') AND Inserted.SERIE_NF not in ('','NULL')

  End
End